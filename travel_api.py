import connexion

# Create a Connexion app (uses Flask underneath)
app = connexion.FlaskApp(__name__)

# Load the OpenAPI spec (defined in travel-api.yml)
app.add_api("travel-api.yml")

# Start the server 
app.run(host="0.0.0.0", port=82, debug=True)
