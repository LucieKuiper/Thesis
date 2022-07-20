from application import db, app


if __name__ == '__main__':
    host='0.0.0.0'
    db.create_all()
    app.run(debug=True)

