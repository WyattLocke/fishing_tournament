from fishing_tournament import app
from fishing_tournament.controllers import user_controller, submission_controller

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')