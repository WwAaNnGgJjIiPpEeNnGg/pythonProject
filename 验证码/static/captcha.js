// Add your JavaScript code for slider interaction here
ddocument.addEventListener('DOMContentLoaded', function () {
  const slider = document.getElementById('slider');
  const submitButton = document.getElementById('submit-button');

  // Function to handle slider movement
  let sliderX = 0;
  let isDragging = false;
  slider.addEventListener('mousedown', function (event) {
    isDragging = true;
    sliderX = event.clientX - slider.getBoundingClientRect().left;
  });
  document.addEventListener('mousemove', function (event) {
    if (isDragging) {
      const sliderPos = event.clientX - sliderX;
      // Ensure the slider stays within the captcha boundaries
      if (sliderPos >= 0 && sliderPos <= (300 - 60)) {
        slider.style.left = `${sliderPos}px`;
      }
    }
  });
  document.addEventListener('mouseup', function (event) {
    if (isDragging) {
      isDragging = false;
      const sliderPos = event.clientX - sliderX;
      // Ensure the slider stays within the captcha boundaries
      if (sliderPos >= 0 && sliderPos <= (300 - 60)) {
        slider.style.left = `${sliderPos}px`;

        // Send the slider position to the backend for verification
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/verify', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4) {
            if (xhr.status === 200) {
              const response = JSON.parse(xhr.responseText);
              if (response.message === 'Success! Captcha passed.') {
                alert('Verification successful!');
              } else {
                alert('Verification failed. Please try again.');
              }
            } else {
              alert('Error occurred. Please try again later.');
            }
          }
        };
        xhr.send(`slider_pos=${sliderPos}`);
      }
    }
  });

  // Function to handle submit button click
  submitButton.addEventListener('click', function () {
    const sliderPos = parseInt(slider.style.left, 10);
    // Send the slider position to the backend for verification
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/verify', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          if (response.message === 'Success! Captcha passed.') {
            alert('Verification successful!');
          } else {
            alert('Verification failed. Please try again.');
          }
        } else {
          alert('Error occurred. Please try again later.');
        }
      }
    };
    xhr.send(`slider_pos=${sliderPos}`);
  });
});
