document.getElementById("fileInput").addEventListener("change", function () {
  const file = this.files[0];
  const previewDiv = document.getElementById("preview");

  if (file) {
    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    img.className = "preview-img";
    img.alt = "Selected Image";
    previewDiv.innerHTML = ""; // Clear previous preview
    previewDiv.appendChild(img);
  }
});

document.getElementById("uploadForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  const resultDiv = document.getElementById("result");

  if (!file) return alert("Please select a file!");

  resultDiv.innerHTML = "🔄 Uploading and analyzing...";

  try {
  const res = await fetch("<My API URL>", {
    method: "GET",
  });


    const { uploadURL, filename } = await res.json();

    await fetch(uploadURL, {
      method: "PUT",
      headers: {
        "Content-Type": file.type,
      },
      body: file,
    });

    resultDiv.innerHTML = `✅ Image uploaded successfully!<br>🔍 Processing started...`;

    localStorage.setItem("uploaded_filename", filename);

    startPolling(filename);
  } catch (err) {
    resultDiv.innerHTML = "❌ Error uploading or analyzing the image.";
    console.error(err);
  }
});

function startPolling(filename) {
  const resultURL = `<My S3 Public Web Hosting URL>/${filename.replace(/\.[^/.]+$/, '')}_result.json`;
  const resultDiv = document.getElementById("result");

  let attempts = 0;
  const maxAttempts = 15;

  const intervalId = setInterval(async () => {
    attempts++;

    try {
      const res = await fetch(resultURL);
      if (res.ok) {
        const data = await res.json();
        const labels = data.Detected_Labels || [];

        resultDiv.innerHTML = `
          ✅ Image processed successfully!<br>
          🔍 Detected Labels (≥ 90% confidence):<br>
          <ul>
            ${labels.map(label => `<li>${label}</li>`).join('')}
          </ul>
        `;

        clearInterval(intervalId);
      }
    } catch (err) {
      // Do nothing
    }

    if (attempts >= maxAttempts) {
      resultDiv.innerHTML = "⚠️ Timed out. Please try again later.";
      clearInterval(intervalId);
    }
  }, 2000);
}

// Resume polling if needed
const savedFilename = localStorage.getItem("uploaded_filename");
if (savedFilename) {
  startPolling(savedFilename);
}
