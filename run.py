from app import create_app

if __name__ == "__main__":
    print("ESTO AQUI ")
    app_flask = create_app()
    print("DEBUG" + str(app_flask.debug))
    app_flask.run()