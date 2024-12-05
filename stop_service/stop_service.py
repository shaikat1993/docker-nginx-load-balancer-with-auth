from flask import Flask, jsonify, request
import os
import subprocess
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def run_bash_script(script_path):
    """Run a bash script and return True if successful."""
    try:
        if not os.path.exists(script_path):
            logging.error(f"Script not found: {script_path}")
            return False
            
        result = subprocess.run(
            ["bash", script_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logging.info("Bash script executed successfully")
            return True
        else:
            logging.error(f"Bash script failed: {result.stderr}")
            return False
            
    except Exception as e:
        logging.error(f"Error running bash script: {str(e)}")
        return False

def run_docker_compose_command(command):
    """Run a docker-compose command and return True if successful."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd="/app"  # Make sure we're in the right directory
        )
        
        if result.returncode == 0:
            logging.info("Docker compose command executed successfully")
            return True
        else:
            logging.error(f"Docker compose command failed: {result.stderr}")
            return False
            
    except Exception as e:
        logging.error(f"Error running docker compose command: {str(e)}")
        return False

@app.route("/api/stop", methods=["POST"])
def stop_all_services():
    try:
        logging.debug("Attempting to stop all services...")
        
        # Stop all containers in the compose project
        stop_cmd = subprocess.run(
            ["docker", "compose", "-f", "/app/docker-compose.yaml", "down"],
            capture_output=True,
            text=True,
            cwd="/app"
        )
        
        if stop_cmd.returncode == 0:
            logging.info("Successfully stopped all services")
            return jsonify({"message": "All services stopped successfully"}), 200
        else:
            # If docker compose fails, try stopping containers directly
            kill_cmd = subprocess.run(
                ["sh", "-c", "docker kill $(docker ps -q)"],
                capture_output=True,
                text=True
            )
            
            if kill_cmd.returncode == 0:
                logging.info("Successfully stopped all containers")
                return jsonify({"message": "All services stopped successfully"}), 200
            else:
                error = f"Failed to stop services: {stop_cmd.stderr}, Kill error: {kill_cmd.stderr}"
                logging.error(error)
                return jsonify({"message": error}), 500
                
    except Exception as e:
        logging.error(f"Error stopping services: {str(e)}")
        return jsonify({"message": f"Error stopping services: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8210)
