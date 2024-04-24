let calorieCount = 0;

function updateCalories(amount) {
  calorieCount += amount;
  const caloriePercentage = (calorieCount / 1750) * 100;
  const calorieBar = document.querySelector('.calorie-bar');
  calorieBar.style.height = `${caloriePercentage}%`;
  const speedometer = document.querySelector('.speedometer');

  if (calorieCount >= 2000) {
    speedometer.classList.remove('above-1750');
    speedometer.classList.add('above-2000');
  } else if (calorieCount >= 1750) {
    speedometer.classList.remove('above-2000');
    speedometer.classList.add('above-1750');
  } else {
    speedometer.classList.remove('above-1750', 'above-2000');
  }

  if (calorieCount >= 1750 && calorieCount < 2000) {
    document.getElementById('faceIcon').className = 'fa-solid fa-face-smile';
    document.getElementById('faceText').textContent = 'Congrats on meeting your calorie requirements!';
  } else if (calorieCount >= 2000) {
    document.getElementById('faceIcon').className = 'fa-solid fa-face-angry';
    document.getElementById('faceText').textContent = 'Exceeding calorie requirements!';
  } else {
    document.getElementById('faceIcon').className = 'fa-solid fa-face-smile';
    document.getElementById('faceText').textContent = 'Keep Going!';
  }

  document.getElementById('calorieCount').textContent = `${calorieCount} / 1750`;
}

function resetCalories() {
  calorieCount = 0;
  document.getElementById('calorieCount').textContent = `${calorieCount} / 1750`;
  document.querySelector('.calorie-bar').style.height = `0%`;
  document.getElementById('faceIcon').className = 'fa-solid fa-face-smile';
  document.getElementById('faceText').textContent = 'Keep Going!';
}

function simulateCalorieAddition(calories) {
  updateCalories(calories);
}

setInterval(() => {
  const now = new Date();
  if (now.getHours() === 0 && now.getMinutes() === 0 && now.getSeconds() === 0) {
    resetCalories();
  }
}, 1000);

// simulateCalorieAddition(500);
// simulateCalorieAddition(1000);
// simulateCalorieAddition(1000);
