// Get elements
const redTile = document.getElementById('red-tile');
const redTile1 = document.getElementById('red1-tile');
const blueTile = document.getElementById('blue-tile');
const blueTile1 = document.getElementById('blue1-tile');
const greenTile = document.getElementById('green-tile');
const notificationArea = document.getElementById('notification-area');

// Add loading bar
let loadingBar; // Define loadingBar globally
eel.expose(showLoadingBar);
function showLoadingBar() {
  loadingBar = document.createElement('div');
  loadingBar.classList.add('loading-bar');
  document.body.appendChild(loadingBar);
}

// Function to add notification
function addNotification(message) {
  // Clear previous notifications
  notificationArea.innerHTML = '';

  const notificationDiv = document.createElement('div');
  notificationDiv.style.backgroundColor = 'rgb(218, 209, 208)';
  if (message == "0") {
    // Add new notification
    notificationDiv.textContent = "Success: Check documents folder";
    notificationDiv.style.borderLeft = '8px solid rgb(166, 207, 99)';
  } else if (message == "1") {
    notificationDiv.textContent = "Something went wrong";
    notificationDiv.style.borderLeft = '8px solid #e7584d';
  } else if (message == "2") {
    notificationDiv.textContent = "Wrong Password";
    notificationDiv.style.borderLeft = '8px solid rgb(156, 79, 65)';
  }
  notificationArea.appendChild(notificationDiv);

  // Remove notification after 5 seconds
  setTimeout(() => {
    notificationDiv.remove();
  }, 5000);
}

// Event listeners for tiles
redTile.addEventListener('click', async function () {
  try {
    let successMsg = await eel.merge_pdf()();
    addNotification(successMsg);
    loadingBar.remove();
  } catch (error) {
    console.error('Error calling eel.open_file:', error);
    addNotification("1");
  }
  // Visual feedback
  this.style.transform = 'scale(0.95)';
  setTimeout(() => {
    this.style.transform = '';
  }, 100);
});

redTile1.addEventListener('click', async function () {
  try {
    let successMsg = await eel.split_pdf()();
    addNotification(successMsg);
    loadingBar.remove();
  } catch (error) {
    console.error('Error calling eel.split_pdf:', error);
    addNotification("1");
  }
  // Visual feedback
  this.style.transform = 'scale(0.95)';
  setTimeout(() => {
    this.style.transform = '';
  }, 100);
});

blueTile.addEventListener('click', async function () {
  try {
    let successMsg = await eel.decrypt_pdf()();
    addNotification(successMsg);
    loadingBar.remove();
  } catch (error) {
    console.error('Error calling eel.decrypt_pdf:', error);
    addNotification("1");
  }
  // Visual feedback
  this.style.transform = 'scale(0.95)';
  setTimeout(() => {
    this.style.transform = '';
  }, 100);
});

blueTile1.addEventListener('click', async function () {
  try {
    let successMsg = await eel.encrypt_pdf()();
    addNotification(successMsg);
    loadingBar.remove();
  } catch (error) {
    console.error('Error calling eel.decrypt_pdf:', error);
    addNotification("1");
  }
  // Visual feedback
  this.style.transform = 'scale(0.95)';
  setTimeout(() => {
    this.style.transform = '';
  }, 100);
});

greenTile.addEventListener('click', async function () {
  try {
    let successMsg = await eel.compress_pdf()();
    addNotification(successMsg);
    loadingBar.remove();
  } catch (error) {
    console.error('Error calling eel.compress_pdf:', error);
    addNotification("1");
  }
  // Visual feedback
  this.style.transform = 'scale(0.95)';
  setTimeout(() => {
    this.style.transform = '';
  }, 100);
});

// Event listener for elements with the 'destination-path' class
const destinationPaths = document.querySelectorAll('.destination-path');

destinationPaths.forEach(destinationPath => {
  destinationPath.addEventListener('click', async function () {
    try {
      await eel.open_dest()();
    } catch (error) {
      console.error('Error calling eel.open_dest:', error);
      addNotification("1");
    }
  });
});

// Add loading bar styles
const loadingBarStyle = document.createElement('style');
loadingBarStyle.innerHTML = `
  .loading-bar {
    position: fixed;
    top: 3px;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, rgba(0, 123, 255, 0.7), rgba(0, 123, 255, 1));
    animation: loading 2s infinite;
  }

  @keyframes loading {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }
`;
document.head.appendChild(loadingBarStyle);

// Add ripple effect to all tiles
const tiles = document.querySelectorAll('.tile');

tiles.forEach(tile => {
  tile.addEventListener('mousedown', function (e) {
    const ripple = document.createElement('span');
    ripple.classList.add('ripple');
    this.appendChild(ripple);

    const x = e.clientX - this.getBoundingClientRect().left;
    const y = e.clientY - this.getBoundingClientRect().top;

    ripple.style.cssText = `
      position: absolute;
      background-color: rgba(255, 255, 255, 0.7);
      border-radius: 50%;
      transform: scale(0);
      animation: ripple 0.6s linear;
      left: ${x}px;
      top: ${y}px;
    `;

    setTimeout(() => {
      ripple.remove();
    }, 600);
  });
});

// Add ripple animation
const style = document.createElement('style');
style.innerHTML = `
  @keyframes ripple {
    to {
      transform: scale(4);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);
