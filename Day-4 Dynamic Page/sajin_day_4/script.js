const hour = new Date().getHours();
let Text = "";

if (hour < 12) {
  Text = "Good Morning 🌅";
} else if (hour < 18) {
  Text = "Good Afternoon ☀️";
} else {
  Text = "Good Evening 🌙";
}

document.getElementById("greeting").innerText = Text;

function changeBackground() {
  const colors = ["#f4a261", "#2a9d8f", "#e76f51", "#264653", "#8ab17d"];
  const rnd = colors[Math.floor(Math.random() * colors.length)];
  document.body.style.backgroundColor = rnd;
}
