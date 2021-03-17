#!/usr/bin/python3

from application.app import create_app, db


def main():
    app = create_app()
    db.create_all(app=app)
    app.run(debug=True)


if __name__ == "__main__":
    main()
