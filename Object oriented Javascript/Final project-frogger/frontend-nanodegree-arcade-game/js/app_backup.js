var tileHeight = 82;
var tileWidth = 101;
// Enemies our player must avoid
var Enemy = function(lane) {
    // Variables applied to each of our instances go here,
    // we've provided one for you to get started

    // The image/sprite for our enemies, this uses
    // a helper we've provided to easily load images
    this.sprite = 'images/enemy-bug.png';
    this.x = 0;
    this.y = lane * tileHeight - 20;;
    this.speed = 0.2;
};

// Update the enemy's position, required method for game
// Parameter: dt, a time delta between ticks
Enemy.prototype.update = function(dt) {
    // You should multiply any movement by the dt parameter
    // which will ensure the game runs at the same speed for
    // all computers.
    this.x *= dt
    this.y *= dt
    // handles collision
    if ((this.x == player.x ) && (this.y == player.y)){
        player.reset();
    }
};

// Draw the enemy on the screen, required method for game
Enemy.prototype.render = function() {
    ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
};

// Now write your own player class
var Player = function() {
    // Variables applied to each of our instances go here,
    // we've provided one for you to get started

    this.sprite = 'images/char-boy.png';
    this.x = 203;
    this.y = 400;
};

Player.prototype.reset = function(){
    this.x = 203;
    this.y = 400;
}

// This class requires an update(), render() and
// a handleInput() method.

Player.prototype.update =  function(dt) {
    // You should multiply any movement by the dt parameter
    // which will ensure the game runs at the same speed for
    // all computers.
    this.x *= dt
    this.y *= dt
};

Player.prototype.render =  function() {
    ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
};

Player.prototype.handleInput = function(input_code){
    switch(input_code){
        case 'left':
            this.x -= 1;
            break;
        case 'up':
            this.y += 1;
            break;
        case 'right':
            this.x += 1;
            break;
        case 'down':
            this.y -=1;
            break;
        default:
            alert("Wrong input code");
    }
        
};


// Now instantiate your objects.
// Place all enemy objects in an array called allEnemies
// Place the player object in a variable called player


allEnemies = [new Enemy(1), new Enemy(2), new Enemy(3)];

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
