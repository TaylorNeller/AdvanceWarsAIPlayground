
var rows = 4;
var cols = 12;
var squareSize = 16;
var canvasHeight = 300;

var gameContainer = document.getElementById("game-container");

var canvasElem = document.getElementById("game");
canvasElem.width = cols*squareSize;
canvasElem.height = rows*squareSize;
canvasElem.style.height = canvasHeight+"px";
var canvas = canvasElem.getContext("2d");


var melee = [[-1,0],[0,1],[1,0],[0,-1]];
var art = [];
for (var r = -3; r <= 3; r++) {
    for (var c = -3; c <= 3; c++) {
        var dist = Math.sqrt(r*r+c*c);
        if (dist > 1 && dist <= 3 && !(Math.abs(r) == 2 && Math.abs(c) == 2)) {
            art.push([r,c]);
        }
    }
}

var dmgMatrix = [ // row = attacker, col = defender
    [.55,.45,.12,.05,.15],
    [.65,.44,.85,.55,.45],
    [.7,.65,.35,.06,.45],
    [.75,.7,.85,.55,.7],
    [.9,.85,.8,.7,.75]
];


var gameElems = {};

var image = new Image();
image.src = 'assets/OSInfantry.png';
var image2 = new Image();
image2.src = 'assets/OSInfantry2.png';
gameElems.OS_Infantry = {"type": 0, "image":image,"exhausted":image2, "move":3, "value":1, "isExhausted":false, "attackSquares":melee, "team":0, "hp":10}

var image = new Image();
image.src = 'assets/OSMech.png';
var image2 = new Image();
image2.src = 'assets/OSMech2.png';
gameElems.OS_Mech = {"type": 1, "image":image,"exhausted":image2, "move":2, "value":3, "isExhausted":false, "attackSquares":melee, "team":0, "hp":10}

var image = new Image();
image.src = 'assets/OSRecon.png';
var image2 = new Image();
image2.src = 'assets/OSRecon2.png';
gameElems.OS_Recon = {"type": 2, "image":image,"exhausted":image2, "move":8, "value":4, "isExhausted":false, "attackSquares":melee, "team":0, "hp":10}

var image = new Image();
image.src = 'assets/OSTank.png';
var image2 = new Image();
image2.src = 'assets/OSTank2.png';
gameElems.OS_Tank = {"type": 3, "image":image,"exhausted":image2, "move":6, "value":7, "isExhausted":false, "attackSquares":melee, "team":0, "hp":10}

var image = new Image();
image.src = 'assets/OSArtillary.png';
var image2 = new Image();
image2.src = 'assets/OSArtillary2.png';
gameElems.OS_Artillary = {"type": 4, "image":image,"exhausted":image2, "move":5, "value":10, "isExhausted":false, "attackSquares":art, "team":0, "hp":10}


var image = new Image();
image.src = 'assets/BMInfantry.png';
var image2 = new Image();
image2.src = 'assets/BMInfantry2.png';
gameElems.BM_Infantry = {"type": 0, "image":image,"exhausted":image2, "move":3,"value":1, "isExhausted":false, "attackSquares":melee, "team":1, "hp":10}

var image = new Image();
image.src = 'assets/BMMech.png';
var image2 = new Image();
image2.src = 'assets/BMMech2.png';
gameElems.BM_Mech = {"type": 1, "image":image,"exhausted":image2, "move":2,"value":3, "isExhausted":false, "attackSquares":melee, "team":1, "hp":10}

var image = new Image();
image.src = 'assets/BMRecon.png';
var image2 = new Image();
image2.src = 'assets/BMRecon2.png';
gameElems.BM_Recon = {"type": 2, "image":image,"exhausted":image2, "move":8,"value":4, "isExhausted":false, "attackSquares":melee, "team":1, "hp":10}

var image = new Image();
image.src = 'assets/BMTank.png';
var image2 = new Image();
image2.src = 'assets/BMTank2.png';
gameElems.BM_Tank = {"type": 3, "image":image,"exhausted":image2, "move":6,"value":7, "isExhausted":false, "attackSquares":melee, "team":1, "hp":10}

var image = new Image();
image.src = 'assets/BMArtillary.png';
var image2 = new Image();
image2.src = 'assets/BMArtillary2.png';
gameElems.BM_Artillary = {"type": 4, "image":image,"exhausted":image2, "move":5,"value":10 , "isExhausted":false, "attackSquares":art, "team":1, "hp":10}

var image = new Image();
image.src = 'assets/road.png';
gameElems.road = {"image":image}

var image = new Image();
image.src = 'assets/red_dot.png';
gameElems.dot = {"image":image}

var image = new Image();
image.src = 'assets/circle.png';
gameElems.circle = {"image":image}

for (var i = 1; i <= 9; i++) {
    var image = new Image();
    image.src = 'assets/hp'+i+'.png';
    gameElems["hp"+i] = {"image":image}
}

var map = new Array(rows).fill(0).map((o, i) => new Array(cols).fill(0));
for (var r = 0; r < rows; r++) {
    for (var c = 0; c < cols; c++) {
        map[r][c] = {"background" : gameElems.road, "unit" : null, "overlay" : null};
    }
}
addUnits();
function drawMap() {
    for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
            var square = map[r][c];
            canvas.drawImage(square.background.image,c*squareSize,r*squareSize);
            if (square.unit != null) {
                canvas.drawImage((square.unit.isExhausted) ? square.unit.exhausted : square.unit.image,c*squareSize,r*squareSize);
                var shownHP = Math.ceil(square.unit.hp);
                if (shownHP != 10) {
                    canvas.drawImage(gameElems['hp'+shownHP].image,c*squareSize+squareSize/2,r*squareSize+squareSize/2);
                }
            }   
            if (square.overlay != null)
                canvas.drawImage(square.overlay.image,c*squareSize,r*squareSize);
        }
    }
}
function addUnits() {
    // setUnit(1,2,gameElems.OS_Infantry)
    // setUnit(3,0,gameElems.OS_Recon)
    // setUnit(0,5,gameElems.OS_Artillary)
    // // setUnit(0,2,gameElems.OS_Tank)
    // setUnit(1,5,gameElems.OS_Mech)
    // setUnit(3,6,gameElems.BM_Infantry)
    // setUnit(3,4,gameElems.BM_Tank)
    // setUnit(2,5,gameElems.BM_Mech)
    // setUnit(3,5,gameElems.BM_Recon)
    // setUnit(1,7,gameElems.BM_Artillary)

    setUnit(0,0,gameElems.OS_Recon);
    setUnit(1,0,gameElems.OS_Tank);
    setUnit(2,0,gameElems.OS_Artillary);
    setUnit(3,0,gameElems.OS_Recon);
    setUnit(0,1,gameElems.OS_Mech);
    setUnit(1,1,gameElems.OS_Infantry);
    setUnit(2,1,gameElems.OS_Infantry);
    setUnit(3,1,gameElems.OS_Mech);

    setUnit(0,cols-1,gameElems.BM_Recon);
    setUnit(1,cols-1,gameElems.BM_Tank);
    setUnit(2,cols-1,gameElems.BM_Artillary);
    setUnit(3,cols-1,gameElems.BM_Recon);
    setUnit(0,cols-2,gameElems.BM_Mech);
    setUnit(1,cols-2,gameElems.BM_Infantry);
    setUnit(2,cols-2,gameElems.BM_Infantry);
    setUnit(3,cols-2,gameElems.BM_Mech);

}
function setUnit(r, c, unit) {
    map[r][c].unit = copy(unit);
}
function copy(unit) {
    if (unit == null)  {
        return null;
    }
    var newUnit = {};
    var keys = Object.keys(unit);
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        newUnit[key] = unit[key];
    }
    return newUnit;
}
// function mapCopy() {
//     var newMap = new Array(rows).fill(0).map((o, i) => new Array(cols).fill(0));
//     for (var r = 0; r < rows; r++) {
//         for (var c = 0; c < cols; c++) {
//             newMap[r][c] = {"background" : gameElems.road, "unit" : null, "overlay" : null};
//             newMap[r][c].unit = copy(map[r][c].unit);
//         }
//     }
//     return newMap;
// }
function mapCopy(oldMap) {
    var newMap = new Array(rows).fill(0).map((o, i) => new Array(cols).fill(0));
    for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
            newMap[r][c] = {"background" : gameElems.road, "unit" : null, "overlay" : null};
            newMap[r][c].unit = copy(oldMap[r][c].unit);
        }
    }
    return newMap;
}

setTimeout(function() { drawMap(); }, 100);

function isValidMove(row, col) { // can the given square be moved
    return row >= 0 
        && col >= 0 
        && row < rows 
        && col < cols
        && map[row][col].unit != null
        && map[row][col].unit.team == turn
        && !map[row][col].unit.isExhausted;
}
function isAccessable(row, col, unit) { // is the square in bounds and can the unit traverse it
    if (unit == null) {
        return true;
    }
    if (!(row >= 0 
        && col >= 0 
        && row < rows 
        && col < cols)) {
            return false;
    }
    if (map[row][col].unit != null) {
        return map[row][col].unit.team == unit.team;
    }
    return true;
}

function moveUnit(fromRow, fromCol, toRow, toCol) {
    var unit = map[fromRow][fromCol].unit;
    map[fromRow][fromCol].unit = null;
    map[toRow][toCol].unit = unit;
} 

function exhaust(row, col) {
    map[row][col].unit.isExhausted = true;
}

function validAttacks(row, col) { // returns a list of the valid squares that can be attacked by the unit
    var validList = [];
    var unit = map[row][col].unit;
    for (var i = 0; i < unit.attackSquares.length; i++) {
        var newR = row+unit.attackSquares[i][0];
        var newC = col+unit.attackSquares[i][1];
        if (newR >= 0 && newR < rows && newC >= 0 && newC < cols) {
            var target = map[newR][newC];
            if (target.unit != null && unit.team != target.unit.team) {
                validList.push([newR, newC]);
            }
        }

    }
    return validList;
}

function isTargetable(attackerR, attackerC, defenderR, defenderC) { // returns if the first row/col can attack the second row/col
    var attackList = validAttacks(attackerR, attackerC);
    for (var i = 0; i < attackList.length; i++) {
        if (attackList[i][0] == defenderR && attackList[i][1] == defenderC) {
            return true;
        }
    }
    return false;
}

function damageEstimation(attackerR, attackerC, defenderR, defenderC) { // returns damage estimation for attack  (bounded range)
    var unit1 = map[attackerR][attackerC].unit;
    var unit2 = map[defenderR][defenderC].unit;
    var attackVal1 = dmgMatrix[unit1.type][unit2.type];
    var attackVal2 = dmgMatrix[unit1.type][unit2.type] + .09;
    var defenseVal = (100-0*unit2.hp)/100;
    var dmg1 = unit1.hp/10 * attackVal1 * defenseVal;
    var dmg2 = unit1.hp/10 * attackVal2 * defenseVal;

    return [Math.floor(100*dmg1), Math.floor(100*dmg2)];
}

function attack(attackerR, attackerC, defenderR, defenderC) {
    var unit1 = map[attackerR][attackerC].unit;
    var unit2 = map[defenderR][defenderC].unit;
    var attackVal = dmgMatrix[unit1.type][unit2.type] + Math.random() * .09;
    var defenseVal = (100-0*unit2.hp)/100;
    var atkDmg = Math.round(2 * unit1.hp * attackVal * defenseVal)/2; // r(4.3*2) = 9, /2 = 4.5
    unit2.hp -= atkDmg;

    if (unit2.hp <= 0) {
        map[defenderR][defenderC].unit = null;
    }
    else if (unit1.type != 4 && unit2.type != 4) {
        var attackVal = dmgMatrix[unit2.type][unit1.type] + Math.random() * .09;
        var defenseVal = (100-0*unit1.hp)/100;
        var atkDmg = Math.round(2 * unit2.hp * attackVal * defenseVal)/2;
        unit1.hp -= atkDmg;


        if (unit1.hp <= 0) {
            map[attackerR][attackerC].unit = null;
        }
    }
}

function canEnd(fromR, fromC, toR, toC) { // basically checks if a unit is trying to end on an illegal square
    if (fromR == toR && fromC == toC) {
        return true;
    }
    else {
        var unit2 = map[toR][toC].unit;
        return unit2 == null;
    }
}

var endText = document.getElementById("gameover_text");
function checkGameOver() {
    teams = [false,false];
    for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
            if (map[r][c].unit != null) {
                teams[map[r][c].unit.team] = true;
            }
        }
    }
    if (!teams[0] || !teams[1]) {
        gameOver = true;
        if (teams[0]) {
            endText.textContent = "Orange Star Wins!";
        }
        else if (teams[1]) {
            endText.textContent = "Blue Moon Wins!";
        }
    }
}



turn = 0;
attackMode = false;
moving = false;
var path = [];
var target = null;
var unit = null;
var blockPixels = canvasHeight/rows;
var gameOver = false;


function hovered(pageX, pageY) { //-----------------------------------------------------------------------------------------------------
    if (!moving && !attackMode) {
        return;
    }

    var col = Math.floor((pageX - canvasElem.offsetLeft) / blockPixels);
    var row = Math.floor((pageY - canvasElem.offsetTop) / blockPixels);


    if (attackMode) {
        tryAttack(row, col);
        return;
    }


    if ((path.length == 0 && !isValidMove(row, col)) || 
        path.length > 0 && !isAccessable(row, col, map[path[0][0]][path[0][1]].unit)) {
        return;
    }

    var same = false;
    for (var i = 0; i < path.length; i++) {
        if (path[i][0] == row && path[i][1] == col) {
            while (path.length > i+1) {
                pathElem = path.pop();
                map[pathElem[0]][pathElem[1]].overlay = null;
                drawMap();
            }
            same = true;
            break;
        }
    }
    
    if (path.length == 0 || 
        (!same && path.length <= map[path[0][0]][path[0][1]].unit.move)
        && (Math.abs(path[path.length-1][0]-row)+Math.abs(path[path.length-1][1]-col) == 1)) {
        path.push([row, col]);

        map[row][col].overlay = gameElems.dot;
        drawMap();
    }
    
}

var dmgElem = document.getElementById("dmg");

function tryAttack(row, col) {
    if (!(row == target[0] && col == target[1])
        && (row == unit[0] && col == unit[1] || isTargetable(unit[0], unit[1], row, col))) {
        
        map[target[0]][target[1]].overlay = null;
        target = [row, col];
        if (row == unit[0] && col == unit[1]) {
            map[row][col].overlay = gameElems.dot;
            dmgElem.textContent = "Damage Range: -";
        }
        else {
            map[row][col].overlay = gameElems.circle;
            var dmgRange = damageEstimation(unit[0], unit[1], row, col);
            dmgElem.textContent = "Damage Range: "+dmgRange[0]+'-'+dmgRange[1]+'%';
        }
        drawMap();
    }
}

function onMouseMove(event) {
    hovered(event.pageX, event.pageY);
}

document.addEventListener('mousemove', onMouseMove);




canvasElem.onmousedown = function(event) {

    if (!gameOver) {
        canvasElem.onmouseup = function() {
            
            var col = Math.floor((event.pageX - canvasElem.offsetLeft) / blockPixels);
            var row = Math.floor((event.pageY - canvasElem.offsetTop) / blockPixels);
    
            if (!moving && !attackMode && isValidMove(row, col)) {
                moving = true;
                hovered(event.pageX, event.pageY)
            }
            else if (path.length > 0 && canEnd(path[0][0], path[0][1], path[path.length-1][0], path[path.length-1][1])) {
    
                if (!attackMode) {
    
                    var from = path[0];
                    var to = path[path.length-1];
            
                    while (path.length > 0) {
                        pathElem = path.pop();
                        map[pathElem[0]][pathElem[1]].overlay = null;
                    }
            
                    moveUnit(from[0],from[1],to[0],to[1]);
                    if (validAttacks(to[0], to[1]).length > 0) {
                        attackMode = true;
                        unit = to;
                        target = unit;
                        path = [unit];
                        map[target[0]][target[1]].overlay = gameElems.dot;
                    }
                    else {
                        exhaust(to[0], to[1]);
                    }
    
                    moving = false;
    
                }
                else {
                    if (!(unit[0] == target[0] && unit[1] == target[1])) {
                        attack(unit[0],unit[1],target[0],target[1]);
                        checkGameOver();
                    }
                    map[target[0]][target[1]].overlay = null;
    
                    if (map[unit[0]][unit[1]].unit != null) {
                        exhaust(unit[0], unit[1]);
                    }
                    attackMode = false;
                    path = [];
                    target = null;
                    unit = null;
                    dmgElem.textContent = "Damage Range: -";
    
                }
                drawMap();
    
            }
    
    
        };
    }
 
  };

turnText = document.getElementById("turn_text");
buttonElem = document.getElementById("end_turn");
buttonElem.onmousedown = function(event) {
    if (!gameOver && !moving && !attackMode) {
        buttonElem.onmouseup = function() {
            endTurnVisual();
        }
    }
}


function endTurn() {
    turn = 1-turn;
    for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
           var unit = map[r][c].unit;
            if (unit != null && unit.isExhausted) {
                unit.isExhausted = false;
            }
        }
    }    
}









var center = null;
function getCenter(player) {
    var Rs = [];
    var Cs = [];
    var weights = [];
    for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
            var unit = map[r][c].unit;
            if (unit != null && unit.team == player) {
                Rs.push(r);
                Cs.push(c);
                weights.push(unit.hp / 10);
            }
        }
    }
    var n = weights.length;
    center = [0,0];
    for (var i = 0; i < n; i++) {
        center[0] += Rs[i]*weights[i]/n;
        center[1] += Cs[i]*weights[i]/n;
    }
}

function heuristic() {
    var score = 0;
    for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
            var unit = map[r][c].unit;
            if (unit != null) {
                score += unit.value * unit.hp / 10 * (unit.team == turn ? 1 : -1);
            }
        }
    }
    return score;
}
function getDistScore(move) {
    return -Math.sqrt(Math.pow(move[2]-center[0],2)+Math.pow(move[3]-center[1],2));
}











var searched = [];
function getLegalMoves() {
    var moves = [];
    for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
            var unit = map[r][c].unit;
            if (unit != null && (unit.team == turn) && !unit.isExhausted) {
                searched = new Array(rows).fill(0).map((o, i) => new Array(cols).fill(-1));
                var newMoves = search(r,c,r,c,unit.move,unit.attackSquares);
                moves = moves.concat(newMoves);
            }
        }
    }
    return moves;
}

function search(oriR, oriC, row, col, dist, atkSquares) {
    var moves = [];
    if (searched[row][col] < dist) {
        // attacks
        if (searched[row][col] == -1 && canEnd(oriR,oriC,row,col)) {
            moves.push([oriR,oriC,row,col,null,null])
            
            var isThere = true;
            var ob = null;
            if (!(oriR == row && oriC == col)) {
                isThere = false;
                ob = copy(map[row][col].unit);
                setUnit(row, col, map[oriR][oriC].unit);
            }
            for (var i = 0; i < atkSquares.length; i++) {
                var newR = row + atkSquares[i][0];
                var newC = col + atkSquares[i][1];
                if (isTargetable(row,col,newR,newC)) {
                    moves.push([oriR,oriC,row,col,newR,newC])
                }
            }
            if (!isThere) {
                map[row][col].unit = ob;
            }
        }
        searched[row][col] = dist;
        //other moves
        for (var i = 0; i < melee.length; i++) {
            var newR = row + melee[i][0];
            var newC = col + melee[i][1];
            if (isAccessable(newR, newC, map[oriR][oriC].unit) && dist > 0) {
                var newMoves = search(oriR, oriC, newR, newC, dist-1, atkSquares);
                moves = moves.concat(newMoves);
            }
        }
    }
    return moves;
}
function makeMove(move) {
    setUnit(move[2],move[3],map[move[0]][move[1]].unit);
    if (!(move[0] == move[2] && move[1] == move[3])) {
        map[move[0]][move[1]].unit = null;
    }
    map[move[2]][move[3]].unit.isExhausted = true;
    if (move[4] != null) {
        attack(move[2],move[3],move[4],move[5]);
    }
}



function takeTurnVisual() {
    move = getNextGreedy();
    // console.log(move);
    if (move != null) {
        makeMove(move);

        drawMap();
        setTimeout(function() { takeTurnVisual(); }, 500);
    }
    else {
        endTurnVisual();
    }
}

function startAITurn() {
    setTimeout(function() { takeTurnVisual(); }, 1000);
}


var greedyMoves = 1000
function startAITurn2() {
    setTimeout(function() { 
        var moves = getGreedyOrder(greedyMoves);
        takeGreedy2TurnVisual(moves);
    }, 1000);
}
function takeGreedy2TurnVisual(moves) {
    if (moves.length != 0) {
        var move = moves.shift();
        if (canEnd(move[0],move[1],move[2],move[3]) 
            && !(move[4] != null && map[move[4]][move[5]].unit == null)) {
            makeMove(move);
            drawMap();
            setTimeout(function() { takeGreedy2TurnVisual(moves); }, 300);
        }
         else {
            console.log('unlucky?')
            moves = getGreedyOrder(greedyMoves);
            setTimeout(function() { takeGreedy2TurnVisual(moves); }, 300);
        }
    }
    else {
        endTurnVisual();
    }
}

function endTurnVisual() {
    endTurn();

    turnText.textContent = "Turn: " + ((turn == 0) ? "Orange Star" : "Blue Moon");
    drawMap();
    if (turn == 0) {
        startAITurn3();
    }
    else if (turn == 1) {
        startAITurn();
    }
}

startAITurn3();

// ---------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------



var baseSteps = 1000;

function startAITurn3() {
    setTimeout(function() { 
        var moves = getMoveOrder(baseSteps);
        takeOrderedTurnVisual(moves);
    }, 1000);

}
function takeOrderedTurnVisual(moves) {
    if (moves.length != 0) {
        var move = moves.shift();
        if (canEnd(move[0],move[1],move[2],move[3]) 
            && !(move[4] != null && map[move[4]][move[5]].unit == null)) {
            makeMove(move);
            drawMap();
            setTimeout(function() { takeOrderedTurnVisual(moves); }, 300);
        }
         else {
            console.log('unlucky?')
            moves = getMoveOrder(baseSteps);
            setTimeout(function() { takeOrderedTurnVisual(moves); }, 300);
        }
    }
    else {
        endTurnVisual();
    }
}

function takeOrderedTurn(steps) {
    var moves = getMoveOrder(steps);
    while (moves.length != 0) {
        var move = moves.shift();
        if (canEnd(move[0],move[1],move[2],move[3]) && !(move[4] != null && map[move[4]][move[5]].unit == null)) {
            makeMove(move);
            if (move[4] == null && move[5] != null) {
                console.log('stopped attack')
            }
        }
        else {
            console.log('unlucky?')
            moves = getMoveOrder(steps);
        }
    }
    endTurn();
}
function getMoveOrder(steps) {
    var thisMap = mapCopy(map);
    var thisTurn = turn;

    var orderedMoves = [];
    var move = getNextGreedy();

    // generate initial ordered list of moves (use greedy)
    while (move != null) {
        orderedMoves.push(move);
        makeMove(move);
        move = getNextGreedy();
    }
    endTurn();


    var bestMoveSet = [...orderedMoves];
    var t1 = performance.now();
    var bestScore = getChunkHeuristic();
    var t2 = performance.now();
    console.log(t2-t1)
    var currMoveSet = [...orderedMoves];
    var currScore = bestScore;
    var epsilon = .1;
    var timeStart = performance.now();
    for (var i = 0; i < steps; i++) {
        // step: pop random move + dependents
        orderedMoves = [...currMoveSet];
        var popNum = Math.floor(Math.random()*orderedMoves.length);
        for (var j = orderedMoves.length-1; j > popNum; j--) {
            if (orderedMoves[j][2] == orderedMoves[popNum][0] 
                && orderedMoves[j][3] == orderedMoves[popNum][1]
                || (orderedMoves[popNum][4] != null 
                    && orderedMoves[j][2] == orderedMoves[popNum][4] 
                    && orderedMoves[j][3] == orderedMoves[popNum][5])) {
                orderedMoves.splice(j,1);
            }
        }
        orderedMoves.splice(popNum,1);
        
        map = mapCopy(thisMap);

        turn = thisTurn;
        
        for (var j = 0; j < orderedMoves.length; j++) {
            if (orderedMoves[j][4] != null && map[orderedMoves[j][4]][orderedMoves[j][5]].unit == null) {
                orderedMoves[j][4] = null;
                // orderedMoves[j][5] = null;
            }
            makeMove(orderedMoves[j]);
        }

        // for each popped, move to random location
        var move = getNextRandom();
        while (move != null) {
            orderedMoves.push(move);
            makeMove(move);
            move = getNextRandom();
        }
        endTurn();

        // evaluate if it is better, if it is, keep it
        var newScore = getChunkHeuristic();

        if (newScore >= currScore || Math.random() < epsilon) {
            currMoveSet = [...orderedMoves];
            currScore = newScore;
            if (newScore >= bestScore) {
                bestMoveSet = [...orderedMoves];
                bestScore = newScore;
            }
        }
    }
    var timeEnd = performance.now();
    console.log("calculation time: "+(timeEnd-timeStart));

    map = thisMap;
    turn = thisTurn;
    return bestMoveSet;
}
function getChunkHeuristic() {
    var nSims = 1;
    var depth = 1;
    var score = 0;
    var thisMap = mapCopy(map);
    for (var j = 0; j < nSims; j++) {
        for (var i = 0; i < depth; i++) {
            // takeBestRandomGreedyTurn(10);
            // takeRandomGreedyTurn();
            // takeRandomBestTurn(50);      //
            // takeRandomTurn();            // not sophisticated at all for move ordering
            takeGreedyTurn();            // ok but does not seem to understand my move ordering - best so far
            // are there bugs keeping it from attacking?
            // takeNewGreedyTurn(10);       // time costly, sometimes stupidly puts stuff forward
        }
        score += heuristic() * (depth % 2 == 1 ? 1 : -1);
        map = mapCopy(thisMap);
    }

    // map = thisMap;

    return score/nSims;
}














function takeMCTurn() {
    var move = getNextMC();
    while (move != null) {
        makeMove(move);
        move = getNextMC();
    }
    endTurn();
}
function getNextMC() {

    var legalMoves = getLegalMoves();
    var bestMove = null;
    var bestScore = -9999;
    for (var i = 0; i < legalMoves.length; i++) {
        var score = getMCScore(legalMoves[i]);


        if (score > bestScore) {
            bestMove = legalMoves[i];
            bestScore = score;
        }
    }
    return bestMove;
}
function getMCScore(move) {
    var thisMap = mapCopy(map);
    makeMove(move);
    for (var i = 0; i < 12; i++) {
        takeGreedyTurn();
    }
    var score = heuristic();
    map = thisMap;

    return score;
}








function takeGreedyTurn() {
    var move = getNextGreedy();
    while (move != null) {
        makeMove(move);
        move = getNextGreedy();
    }
    endTurn();
}
function takeRandomGreedyTurn() {
    var move = getNextGreedy();
    while (move != null) {
        makeMove(move);
        move = getNextRandomGreedy();
    }
    endTurn();
}
function getNextRandomGreedy() {

    var legalMoves = getLegalMoves();
    var unitMove = Math.floor(Math.random()*legalMoves.length);
    var newMoves = [];
    for (var i = 0; i < legalMoves.length; i++) {
        if (legalMoves[i][0] == legalMoves[unitMove][0]
            && legalMoves[i][1] == legalMoves[unitMove][0]) {
                newMoves.push(legalMoves[i]);
            }
    }
    legalMoves = newMoves;

    var bestMoves = [];
    var bestScore = -9999;
    for (var i = 0; i < legalMoves.length; i++) {
        if (legalMoves[i][4] != null) {
            var score = getGreedyScore(legalMoves[i]);

            if (score > bestScore) {
                bestMoves.push(legalMoves[i]);
                bestScore = score;
            }
        }
    }
    if (bestMoves.length > 0) {
        return bestMoves[bestMoves.length-(1+Math.floor(Math.random()*3))];
    }
    else {
        getCenter(1-turn);
        for (var i = 0; i < legalMoves.length; i++) {
            var score = getDistScore(legalMoves[i]);

            if (score > bestScore) {
                bestMoves.push(legalMoves[i]);
                bestScore = score;
            }
        }
        return bestMoves.length == 0 ? null : bestMoves[bestMoves.length-(1+Math.floor(Math.random()*3))];
    }
}
function getNextGreedy() {

    var legalMoves = getLegalMoves();
    var bestMoves = [];
    var bestScore = -9999;
    for (var i = 0; i < legalMoves.length; i++) {
        if (legalMoves[i][4] != null) {
            var score = getGreedyScore(legalMoves[i]);

            if (score > bestScore) {
                bestMoves.push(legalMoves[i]);
                bestScore = score;
            }
        }
    }
    if (bestMoves.length > 0) {
        return bestMoves[bestMoves.length-1];
    }
    else {
        var bestMove = null;
        getCenter(1-turn);
        for (var i = 0; i < legalMoves.length; i++) {
            var score = getDistScore(legalMoves[i]);

            if (score > bestScore) {
                bestMove = legalMoves[i];
                bestScore = score;
            }
        }
        return bestMove;
    }
}
function getGreedyScore(move) {
    var thisMap = mapCopy(map);
    makeMove(move);
    var score = heuristic();
    map = thisMap;

    return score;
}

function getNextRandom() {
    var legalMoves = getLegalMoves();
    return legalMoves.length == 0 ? null : legalMoves[Math.floor(Math.random() * legalMoves.length)];
}
function takeRandomTurn() {
    var move = getNextRandom();
    while (move != null) {
        makeMove(move);
        move = getNextRandom();
    }
    endTurn();
}


//TODO:
// enhance greedy player:   see 1 turn ahead
//                          take best combo available
//                                  solution: optimizer
// test epsilon

function takeNewGreedyTurn(steps) {
    var moves = getGreedyOrder(steps);
    while (moves.length != 0) {
        var move = moves.shift();
        if (canEnd(move[0],move[1],move[2],move[3]) && !(move[4] != null && map[move[4]][move[5]].unit == null)) {
            makeMove(move);
        }
        else {
            // console.log('unlucky2?')
            moves = getGreedyOrder(steps);
        }
    }
    endTurn();
}
function getGreedyOrder(steps) {
    var thisMap = mapCopy(map);
    var thisTurn = turn;

    var orderedMoves = [];
    var move = getNextGreedy();

    // generate initial ordered list of moves (use greedy)
    while (move != null) {
        orderedMoves.push(move);
        makeMove(move);
        move = getNextGreedy();
    }
    endTurn();


    var bestMoveSet = [...orderedMoves];
    var bestScore = newGreedyHeuristic();
    var currMoveSet = [...orderedMoves];
    var currScore = bestScore;
    var epsilon = 0;
    // var timeStart = performance.now();
    for (var i = 0; i < steps; i++) {
        // step: pop random move + dependents
        orderedMoves = [...currMoveSet];
        var popNum = Math.floor(Math.random()*orderedMoves.length);
        for (var j = orderedMoves.length-1; j > popNum; j--) {
            if (orderedMoves[j][2] == orderedMoves[popNum][0] 
                && orderedMoves[j][3] == orderedMoves[popNum][1]
                || (orderedMoves[popNum][4] != null 
                    && orderedMoves[j][2] == orderedMoves[popNum][4] 
                    && orderedMoves[j][3] == orderedMoves[popNum][5])) {
                orderedMoves.splice(j,1);
            }
        }
        orderedMoves.splice(popNum,1);
        
        map = mapCopy(thisMap);
        turn = thisTurn;
        
        for (var j = 0; j < orderedMoves.length; j++) {
            if (orderedMoves[j][4] != null && map[orderedMoves[j][4]][orderedMoves[j][5]].unit == null) {
                orderedMoves[j][4] = null;
                orderedMoves[j][5] = null;
            }
            makeMove(orderedMoves[j]);
        }

        // for each popped, move to random location
        var move = getNextRandom();
        while (move != null) {
            orderedMoves.push(move);
            makeMove(move);
            move = getNextRandom();
        }
        endTurn();

        // evaluate if it is better, if it is, keep it
        var newScore = newGreedyHeuristic();
        if (newScore >= currScore || Math.random() < epsilon) {
            currMoveSet = [...orderedMoves];
            currScore = newScore;
            if (newScore >= bestScore) {
                bestMoveSet = [...orderedMoves];
                bestScore = newScore;
            }
        }
    }
    // var timeEnd = performance.now();
    // console.log("performance2: "+(timeEnd-timeStart))

    map = thisMap;
    turn = thisTurn;
    return bestMoveSet;
}

function newGreedyHeuristic() {
    takeGreedyTurn();
    return heuristic()
}

function takeRandomBestTurn(steps) {
    var thisMap = mapCopy(map);
    var bestMap = null;
    var bestScore = -9999;
    for (var i = 0; i < steps; i++){
        var move = getNextRandom();
        while (move != null) {
            makeMove(move);
            move = getNextRandom();
        }
        var newScore = heuristic();
        if (newScore > bestScore) {
            bestMap = mapCopy(map);
            bestScore = newScore;
        }
        map = mapCopy(thisMap);
    }
    map = bestMap;
}

function takeBestRandomGreedyTurn(steps) {
    var thisMap = mapCopy(map);
    var bestMap = null;
    var bestScore = -9999;
    for (var i = 0; i < steps; i++){
        takeRandomGreedyTurn();
        turn = 1-turn;
        var newScore = heuristic();
        if (newScore > bestScore) {
            bestMap = mapCopy(map);
            bestScore = newScore;
        }
        map = mapCopy(thisMap);
    }
    map = bestMap;
}