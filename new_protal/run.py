from routes import app, user_db, centremanager


if __name__ == '__main__':
    # SIGINT to stop (Ctrl + C)
    app.run(debug=True)

    # Saves the data
    print('Saving...')
    user_db.save_data()
    centremanager.save_data()
    print('Save complete')
