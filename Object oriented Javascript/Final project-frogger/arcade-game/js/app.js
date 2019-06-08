// constants

var tileHeight = 82;
var tileWidth = 101;
var upMovement = -1 * tileHeight;
var leftMovement = -1 * tileWidth;
var laneSpeed = [70, 100, 175, 150, 125, 100];
var canvasWidth = 505;
var canvasHeight = 606;
var offset = 20;
var collisionOffsetX = 70;
var collisionOffsetY = 20;
var playerOriginX = 202;
var playerOriginY = 405;
var playerLives = 3;
var resetEnemyX = -10;
var playerInWaterY = -5;

// Todo
// group constants
// timed game

// Enemies our player must avoid
var Enemy = function(lane) {
    // Variables applied to each of our instances go here,
    // we've provided one for you to get started

    // The image/sprite for our enemies, this uses
    // a helper we've provided to easily load images
    this.x = 0;
    this.y = lane * tileHeight - offset;
    this.sprite = 'images/enemy-bug.png';
    this.speed = laneSpeed[lane - 1];
};

// Update the enemy's position, required method for game
// Parameter: dt, a time delta between ticks
Enemy.prototype.update = function(dt) {
    // You should multiply any movement by the dt parameter
    // which will ensure the game runs at the same speed for
    // all computers.
    this.x += this.speed * dt
    if (this.x > canvasWidth + offset){ // dont go off screen
         this.reset();
    };

    // check for collisions

    const differenceX = Math.abs(player.x - this.x);
    const differenceY = Math.abs(player.y - this.y);

    if(differenceX < collisionOffsetX && differenceY < collisionOffsetY){
        player.lives -= 1;
        if (player.lives <= 0){
            alert("Game over!")
        }
        player.reset();
        
        
    };

};

Enemy.prototype.reset = function(){
    this.x = resetEnemyX;
}
// Draw the enemy on the screen, required method for game
Enemy.prototype.render = function() {
    ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
};

// Now write your own player class
// This class requires an update(), render() and
// a handleInput() method.

var Player = function(){
    this.x = playerOriginX;
    this.y = playerOriginY;
    this.lives = playerLives;
    this.sprite  = 'images/char-boy.png';
};

Player.prototype.update = function(dt) {

};

// Draw the enemy on the screen, required method for game
Player.prototype.render = function() {
    ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
};

Player.prototype.reset = function() {
    this.x = playerOriginX;
    this.y = playerOriginY;
};

Player.prototype.handleInput = function(input_code){
    switch(input_code){
        case 'left':
            this.x += leftMovement;
            if (this.x < 0){
                this.x += tileWidth;
            };
            break;
        case 'up':
            this.y += upMovement;
            if (this.y == playerInWaterY){
                alert("Game, won!");
                player.reset();
            }
            break;
        case 'right':
            this.x -= leftMovement;
            if (this.x > canvasWidth - offset){
                this.x -= tileWidth;
            };
            break;
        case 'down':
            this.y -= upMovement;
            if (this.y > 462 - tileHeight - offset){ // edit
                this.y = 405; // edit
            };
            break;
        default:
            alert("Wrong input code");
    }
        
};


// Now instantiate your objects.
// Place all enemy objects in an array called allEnemies
// Place the player object in a variable called player

allEnemies = [new Enemy(1), new Enemy(2)];
player = new Player();

// This listens for key presses and sends the keys to your
// Player.handleInput() method. You don't need to modify this.
document.addEventListener('keyup', function(e) {
    var allowedKeys = {
        37: 'left',
        38: 'up',
        39: 'right',
        40: 'down'
    };

    player.handleInput(allowedKeys[e.keyCode]);
});