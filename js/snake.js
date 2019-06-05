const button = document.getElementById("play");
const score = document.getElementById("score");
const canvas = document.getElementById("draw-board");

const ctx = canvas.getContext("2d");

// game state
var state = {

  gameover: true,

  direction: 2,

  snake: [
    { x: 10, y: 10, direction: 2 },
    { x: 10, y: 20, direction: 2 },
    { x: 10, y: 30, direction: 2 }
  ],

  food: {x: 0, y: 0},

  score: 0
}

// draw section

function drawSnakePart(ctx, x, y, head=False) {

  ctx.fillStyle = head ? "red":"white";

  ctx.fillRect(x, y, 10, 10);

}

function drawFood(ctx, x, y) {

  ctx.beginPath();

  ctx.fillStyle="green";

  ctx.arc(x+5, y+5, 5, 0, 2 * Math.PI);

  ctx.stroke();

  ctx.fill();
}

function drawBackground() {

  ctx.fillStyle = "tan";

  ctx.fillRect(0, 0, 250, 250);
}

function drawSnake() {

  for (let i = state.snake.length - 1; i >= 0; --i) {
    drawSnakePart(ctx, state.snake[i].x, state.snake[i].y, i === 0);
  }
}

function mod(m, val) {
  while (val < 0) {
    val += m;
  }
  return val % m;
}

function addPart() {

  let tail = state.snake[state.snake.length -1];

  let direction = tail.direction;
  let x = tail.x;
  let y = tail.y;

  switch (direction) {

    case 1:
      y = mod(250, y - 10);
      break;

    case -1:
      y = mod(250, y +10);
      break;

    case -2:
      x = mod(250, x + 10);
      break;

    case 2:
      x = mod(250, x - 10);
      break;

  }
  state.snake.push({x, y, direction });
}

function eatFood() {

  let x = state.snake[0].x;
  let y = state.snake[0].y;

  let fx = state.food.x;
  let fy = state.food.y;

  if (x == fx && y == fy) {

    state.score++;

    score.innerHTML = "Score: " + state.score;

    addPart();

    generateFood();

  }
}

function moveSnake() {

  let x = state.snake[0].x;
  let y = state.snake[0].y;

  switch (state.direction) {

    case 1:
      y = mod(250, y + 10);
      break;

    case -1:
      y = mod(250, y - 10);
      break;

    case -2:
      x = mod(250, x - 10);
      break;

    case 2:
      x = mod(250, x + 10);
      break;

  }

  const newSnake = [{ x, y, direction:state.direction }];

  const snakeLength = state.snake.length;

  for (let i = 1; i < snakeLength; ++i){
    newSnake.push({...state.snake[i - 1] });
  }

  state.snake = newSnake;
}

function checkGameOver() {
  const head = state.snake[0];

  return state.snake.some(
    (part, i) => i !== 0 && head.x === part.x && head.y === part.y
  );
}

function generateFood() {
  let x = Math.floor(Math.random() * 25) * 10;
  let y = Math.floor(Math.random() * 25) * 10;

  while (state.snake.some(part => part.x === x && part.y === y)) {
    x = Math.floor(Math.random() * 25) *10;
    y = Math.floor(Math.random() * 25) * 10;
  }

  state.food = { x, y};

}

var start = 0;

function draw(timestamp) {

  start++;

  if (timestamp - start > 1000 / 10) {

    if (checkGameOver()) {

      state.gameover = true;
      return;
    }

    moveSnake();

    drawBackground();

    drawFood(ctx, state.food.x, state.food.y);

    drawSnake();

    eatFood();

    start = timestamp;
  }

  if (!state.gameover) window.requestAnimationFrame(draw);
}

// event handling

document.addEventListener("keydown", event => {

  if (!/Arrow/gi.test(event.key))

  return;

  event.preventDefault();

  let direction = 0;

  switch (event.key) {

    case "ArrowDown":
      direction = 1;
      break;

    case "ArrowUp":
      direction = -1;
      break;

    case "ArrowLeft":
      direction = -2;
      break;

    case "ArrowRight":
      direction = 2;
      break;
  }

  if (
    direction &&

    state.direction === state.snake[0].direction &&

    state.direction !== -direction
  ) {
    state.direction = direction;
  }
});

// event handler

play.onclick = function() {

  if (state.gameover) {

    state = {
      gameover: false,
      direction: 2,

      snake: [
        {x: 10, y: 10, direction: 2 },
        {x: 10, y: 20, direction: 2 },
        {x: 10, y: 30, direction: 2 }
      ],

      food: {x:0, y: 0},

      score: 0
    };

    score.innerHTML = "Score: " + 0;

    generateFood();

    window.requestAnimationFrame(draw);
  }
};
