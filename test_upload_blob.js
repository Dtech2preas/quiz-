async function testUpload() {
  const blob = new Blob(["test"], { type: 'text/plain' });
  const formData = new FormData();
  formData.append("image", blob);

  const res = await fetch(`https://api.imgbb.com/1/upload?key=cedf418c6d844af9c47a7775a17161a6`, {
    method: "POST",
    body: formData
  });
  console.log(await res.json());
}
testUpload();
