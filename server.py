from app import app
from app.settings import DEBUG


if __name__ == '__main__':
    app.run(debug=DEBUG)