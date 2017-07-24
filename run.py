from app import app
import os


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %s" % port) 

    app.run(debug=True, port=port, host='0.0.0.0')
