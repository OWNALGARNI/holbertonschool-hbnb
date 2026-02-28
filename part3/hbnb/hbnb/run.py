from app import create_app

app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Starting HBnB API Server")
    print("=" * 50)
    print("📍 Server: http://127.0.0.1:5000")
    print("📖 API Docs: http://127.0.0.1:5000/api/v1/")
    print("=" * 50)
    app.run(host='127.0.0.1', port=5000, debug=True)
