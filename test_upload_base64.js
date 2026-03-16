async function testUpload() {
  const formData = new FormData();
  // Valid base64 image (1x1 transparent png)
  formData.append("image", "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=");

  const res = await fetch(`https://api.imgbb.com/1/upload?key=cedf418c6d844af9c47a7775a17161a6`, {
    method: "POST",
    body: formData
  });
  console.log(await res.json());
}
testUpload();
