🛠️ Developer Notes
This is a Serverless Image Analysis Web App.

It lets users upload an image from the browser → sends it to S3 → triggers AWS Rekognition → then shows labels detected with 90%+ confidence.

📁 Project Structure

/frontend       → HTML, JS, and CSS (User interface)
/lambda         → Lambda function for generating presigned URLs and image analysis

🔐 Sensitive Data
✅ API Gateway URLs and S3 website endpoints are not hardcoded in the frontend.
You should add your own when setting it up (see README.md for where).

💡 Usage Flow (Simplified)
User uploads an image from the browser.

JS fetches a presigned URL from your Lambda.

That image is PUT to S3 via that URL.

Another Lambda processes it using Rekognition.

Processed result is saved in a second S3 bucket.

JS polls for the result and displays it on screen.