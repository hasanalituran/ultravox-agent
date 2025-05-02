from flask import Flask, request, Response, jsonify
from twilio.twiml.voice_response import VoiceResponse
from tools import retrieve_from_vector_store
import json
from agent_mapper import AgentMapper
from ultravox_service import create_ultravox_call, create_ultravox_call_with_agent, create_agent, list_agents

app = Flask(__name__)
port = 3000

global agent_service_mapper
agent_mapper = AgentMapper()
 
# create an default endpoint to check if the server is running
@app.route('/', methods=['GET'])
def index():
    return "Server is running!"

@app.route('/list-agents', methods=['GET'])
def list_agents_endpoint():
    response = list_agents()
    if response:
        return jsonify({"result": response}), 200
    else:
        return jsonify({"error": "Failed to list agents"}), 500

@app.route('/create-agent', methods=['POST'])
def create_agent_endpoint():
    response = create_agent()
    return jsonify({"result": response }), 200

@app.route('/incoming', methods=['POST'])
def incoming_call():
    params = request.form.to_dict()
    print(f"Incoming call: {json.dumps(params)}")
    try:
        print("Incoming call received")
        # ultravox_response = create_ultravox_call()

        # TODO: get agent id from the DB mapped to the phone number
        
        called_service_number = params["Called"]
        call_sid = params["AccountSid"]

        agent_id = agent_mapper.get_service_agent_id(called_service_number, call_sid)
        print("Agent ID:", agent_id)

        ultravox_response = create_ultravox_call_with_agent(agent_id)

        join_url = ultravox_response['joinUrl']

        twiml = VoiceResponse()
        connect = twiml.connect()
        connect.stream(url=join_url, name='ultravox')

        return Response(str(twiml), mimetype='text/xml')

    except Exception as e:
        print("Error handling incoming call:", str(e))
        twiml = VoiceResponse()
        twiml.say("Sorry, there was an error connecting your call.")
        return Response(str(twiml), mimetype='text/xml')

@app.route('/retrieve', methods=['POST'])
async def query():
    """
    Endpoint to handle incoming queries.
    """
    print("Received request at /retrieve")
    params = request.get_json() # request.form.to_dict()
    print("Received data:", json.dumps(params))
    try:
        query = params['query']
        if not query:
            return jsonify({"error": "Query parameter is required"}), 400

        # Call the tool to retrieve from vector store
        response = await retrieve_from_vector_store(query)
        if not response:
            return jsonify({"error": "No results found"}), 404
        
        return jsonify({"result": response}), 200

    except Exception as e:
        print("Error handling query:", str(e))
        return "Error processing your request", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=True)