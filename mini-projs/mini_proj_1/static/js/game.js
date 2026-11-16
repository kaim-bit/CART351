let playerR = 16;
let smileEnemySize = 52;
const smileEnemyCount = 3;
let player;
let smileEnemies = [];
let smileEnemyImages = [];
let timeAlive = 0;
let start = 0;
let ended = false;
let saveRequest;

function setup() {
    const gameBox = document.getElementById("game-canvas");

    const canvas = createCanvas(
        gameBox.clientWidth - 6,
        gameBox.clientHeight - 6
    );
    canvas.parent("game-canvas");
    gameBox.style.position = "relative";


    player = createVector(width / 2, height - 45);

    for (let i = 0; i < smileEnemyCount; i += 1) {
        const image = document.createElement("img");
        image.src = window.smileEnemyGifUrl;
        image.alt = "";
        image.className = "smile-enemy";
        image.style.width = `${smileEnemySize}px`;
        image.style.height = `${smileEnemySize}px`;
        const smileEnemy = {
            x: random(0, width - smileEnemySize),
            y: random(0, height / 2),
            speed: random(2, 4)
        };
        image.style.left = `${smileEnemy.x}px`;
        image.style.top = `${smileEnemy.y}px`;

        gameBox.appendChild(image);
        smileEnemyImages.push(image);
        smileEnemies.push(smileEnemy);
    }

    start = millis();
    saveRequest = fetchSData();
    fetchSurveyCount();
}


function windowResized() {
    // this was complicated i had to look this up because of streching problems, 
    const gameBox = document.getElementById("game-canvas");
    const newW = gameBox.clientWidth - 6;
    const newH = gameBox.clientHeight - 6;
    if (newW <= 0 || newH <= 0 || (newW === width && newH === height)) {
        return;
    }

    const scaleX = newW / width;
    const scaleY = newH / height;
    const sizeScale = Math.min(scaleX, scaleY);
    player.x *= scaleX;
    player.y *= scaleY;
    playerR *= sizeScale;
    smileEnemySize *= sizeScale;
    smileEnemies.forEach((smileEnemy) => {
        smileEnemy.x *= scaleX;
        smileEnemy.y *= scaleY;
        smileEnemy.speed *= scaleY;
    });

    resizeCanvas(newW, newH);
    smileEnemyImages.forEach((image) => {
        image.style.width = `${smileEnemySize}px`;
        image.style.height = `${smileEnemySize}px`;
    });
}

function draw() {
    background(0, 0, 0);

    if (!ended) {
        movePlayer();
        updateSmileEnemies();

        timeAlive = floor((millis() - start) / 1000);
        if (timeAlive > 60) {
            ended = true;
            finishGame();
            // i had bug so this stays, 
        } else {
            checkCollisions();
        }
    }

    drawPlayer();
    drawTimeStuff();
}

function movePlayer() {
    //simple movement
    const speed = 4;
    if (keyIsDown(LEFT_ARROW) || keyIsDown(65)) player.x -= speed;
    if (keyIsDown(RIGHT_ARROW) || keyIsDown(68)) player.x += speed;
    if (keyIsDown(UP_ARROW) || keyIsDown(87)) player.y -= speed;
    if (keyIsDown(DOWN_ARROW) || keyIsDown(83)) player.y += speed;

    player.x = constrain(player.x, playerR, width - playerR);
    player.y = constrain(player.y, playerR, height - playerR);
}

function updateSmileEnemies() {
    // through the summons that happened in setup this just manages the actual enemys, there movement and all of that

    smileEnemies.forEach((smileEnemy, index) => {
        smileEnemy.y += smileEnemy.speed;


        if (smileEnemy.y > height) {
            smileEnemy.y = random(-140, -smileEnemySize);
            smileEnemy.x = random(0, width - smileEnemySize);
            smileEnemy.speed = random(2, 4) + timeAlive * 0.04;
        }

        smileEnemyImages[index].style.left = `${smileEnemy.x}px`;
        smileEnemyImages[index].style.top = `${smileEnemy.y}px`;
    });
}

function checkCollisions() {
    for (const smileEnemy of smileEnemies) {
        const nearestX = constrain(player.x, smileEnemy.x, smileEnemy.x + smileEnemySize);
        const nearestY = constrain(player.y, smileEnemy.y, smileEnemy.y + smileEnemySize);

        //if hit
        if (dist(player.x, player.y, nearestX, nearestY) < playerR) {
            ended = true;
            finishGame();
            return;
        }
    }
}

async function finishGame() {
    try {
        await saveRequest;
    } catch (error) {
        console.error("Could not save survey answers:", error);
    }

    const form = document.getElementById("game-results-form");
    document.getElementById("time-alive").value = timeAlive;
    form.submit();
}


async function fetchSData() {
    // Checks that all answers exist, then sends them to Flask to be saved.
    const hasAnswers = Object.values(window.surveyAnswers).every(
        (answer) => answer.trim().length > 0
    );

    if (hasAnswers) {
        const response = await fetch(window.surveyUrlThing, {
            method: "POST",
            headers: { "Content-Type": "application/json" },

            body: JSON.stringify({ answers: window.surveyAnswers })
        });
        if (!response.ok) {
            throw new Error(`Saving survey answers failed (${response.status}).`);
        }
    }
}

async function fetchSurveyCount() {
    try {
        const response = await fetch(window.surveyRetrieveThing);
        if (!response.ok) {
            throw new Error(`Retrieving survey count failed (${response.status}).`);
        }
        await response.json();
    } catch (error) {
        console.error("Could not retrieve survey count:", error);
    }
}


function drawPlayer() {
    noStroke();
    fill(14, 120, 200);
    circle(player.x, player.y, playerR * 2);
}

function drawTimeStuff() {
    //displays time obv
    fill(34, 40, 44);
    textAlign(LEFT, TOP);
    textSize(16);
    text(`Time: ${timeAlive}s`, 12, 12);
}
