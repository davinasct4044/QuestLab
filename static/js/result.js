document.addEventListener("DOMContentLoaded", () => {

    const circle = document.querySelector(".score-circle");

    if (!circle) return;

    const scoreText = document.getElementById("score-value");

    const target = Number(
        circle.dataset.score
    );

    let current = 0;

    const interval = setInterval(() => {

        current++;

        const degrees = current * 3.6;

        circle.style.background =
            `conic-gradient(
                #33F2A0 ${degrees}deg,
                #e2e8f0 ${degrees}deg
            )`;

        scoreText.textContent =
            `${current}%`;

        if(current >= target){

            clearInterval(interval);
        }

    }, 15);

});