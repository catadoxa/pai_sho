<template>
    <div>
        <div class="margin-10 board-container">
            <Space v-for="(space, index) in board"
                    :key="`space-${index}`"
                    :space="space"
                    :piece_selected="state.piece_selected"
                    :locked="state.locked"
                    @move="move"
                    @select="select"
                    />
            <div class="background-container"></div>
            <Winner v-if="winner != null" :winner="winner" />
        </div>
        <GamePanel @end-turn="end_turn"
                    :endTurnDisabled="state === null ? true : !state.current_move"
                    :player="state === null ? 'unknown' : state.players[state.player_moving].name"
                    />
    </div>
</template>

<script>
import GamePanel from './GamePanel.vue'
import Space from './Space.vue'
import Winner from './Winner.vue'

export default {
    name: 'Board',
    components: {
        GamePanel,
        Space,
        Winner,
    },
    data: function() { 
        return {
            board: null, 
            state: null, 
            move_matrix: null, 
            take_matrix: null,
            winner: null,
            move_types: { SINGLE: 1, JUMP: 2, END_TURN: 3, REGENERATE_AVATAR: 4 }
        }
    },
    mounted: function() {
        function make_state(game) {
            return {
                turn_number: game.turn_number,
                players: game.players, 
                player_moving: game.player_moving,
                piece_selected: null, 
                pieces: game.board.pieces, 
                locked: false,
                moves: game.moves, 
                current_move: game.current_move
            };
        }

        function fill_spaces(state, spaces) {
            for(var i = 0; i < state.pieces.length; i++) {
                var space = spaces.find(function(el) {
                    return el.x == state.pieces[i].x && el.y == state.pieces[i].y;
                });
                if(space != null) {
                    space.has_piece = true;
                    space.piece = state.pieces[i];
                }
            }
        }
        
        //use this to load inital state directly from json instead of api
        //import game from '../assets/initial_game.json'
        // this.board = game.board.spaces;
        // this.state = make_state(game);
        // this.take_matrix = game.take_matrix;
        // this.move_matrix = game.move_matrix;
        // this.winner = game.winner;
        // fill_spaces(this.state, this.board);
        // this.make_pieces_selectable();

        const initialUrl = "http://localhost:5000/api/get-initial-setup";

        fetch(initialUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error("HTTP error " + response.status);
                }
                return response.json();
            })
            .then(game => {
                console.log(this);
                this.game = game;
                this.board = game.board.spaces;
                this.state = make_state(game);
                this.take_matrix = game.take_matrix;
                this.move_matrix = game.move_matrix;
                this.winner = game.winner;
                fill_spaces(this.state, this.board);
                this.make_pieces_selectable();
            })
            .catch(function () {
                console.log('error');
            })

    },
    methods: {
        add_step: function(move_type, takes, from_space, to_space) {
            this.state.current_move.steps.push({
                move_type: move_type,
                step_number: this.state.current_move.total_steps++,
                takes: !takes ? null : takes.map(t => this.copy_json(t)),
                initial_position: !from_space ? null : {x: from_space.x, y: from_space.y},
                final_position: !to_space ? null : {x: to_space.x, y: to_space.y}
            });
        },
        move: function(value) {
            if(!this.state.current_move) {
                this.state.current_move = this.generate_move(value.piece, this.state.player_moving);
            }
            this.state.locked = true;
            value.move_to.selected = true;
            var old_space = this.find_space(value.piece.x, value.piece.y);
            var distance = (value.move_to.x - value.piece.x)*(value.move_to.x - value.piece.x)
                        + (value.move_to.y - value.piece.y)*(value.move_to.y - value.piece.y);
            value.piece.x = value.move_to.x;
            value.piece.y = value.move_to.y;
            value.move_to.has_piece = true;
            value.move_to.piece = value.piece;
            old_space.has_piece = false;
            old_space.piece = null;
            old_space.selected = false;
            var enemies_taken = this.take_pieces(value.piece);

            this.restore_avatar();

            if(distance <= 4 || this.state.piece_selected.element === 'LOTUS') {
                this.add_step(this.move_types.SINGLE, enemies_taken, old_space, value.move_to);
                this.add_step(this.move_types.END_TURN);
                this.end_turn();
            } else {
                this.make_jumps_selectable(old_space);
                this.add_step(this.move_types.JUMP, enemies_taken, old_space, value.move_to);
            }
            if(this.board.filter(s => s.selectable === true).length === 0) {
                this.add_step(this.move_types.END_TURN);
                this.end_turn();
            }
        },
        make_jumps_selectable: function(old_space) {
            for(let i = 0; i < this.board.length; i++) {
                this.board[i].selectable = false;
            }
            const x = this.state.piece_selected.x;
            const y = this.state.piece_selected.y;
            for(let i = 0; i < this.move_matrix.length; i++) {
                var space = this.find_space(x + this.move_matrix[i].x, y + this.move_matrix[i].y);
                if(space != null && space.has_piece && space.piece.player_number === this.state.player_moving) {
                    var jump_space = this.find_space(space.x + this.move_matrix[i].x, space.y + this.move_matrix[i].y);
                    if(jump_space != null && !jump_space.has_piece) {
                        jump_space.selectable = true;
                    }
                }
            }
            old_space.selectable = false;
        },
        get_enemies: function(space) {
            var enemies = [];
            for(var i = 0; i < this.move_matrix.length; i++) {
                var test = this.find_space(space.x + this.move_matrix[i].x, space.y + this.move_matrix[i].y);
                if(test && test.has_piece && test.piece.player_number !== this.state.player_moving) {
                    enemies.push(test.piece);
                }
            }
            return enemies;
        },
        end_turn: function() {
            var oldLotus = this.get_lotus(this.state.player_moving);
            if(oldLotus.x === 0 && oldLotus.y === 0) {
                this.declare_winner(this.state.player_moving);
                return;
            }
            this.state.piece_selected = null;
            this.state.locked = false;
            for(var i = 0; i < this.board.length; i++) {
                this.board[i].selected = false;
                this.board[i].selectable = false;
            }
            var nextPlayerNumber = this.swap_player(this.state.player_moving);
            var oldPlayerNumber = this.state.player_moving;
            this.state.player_moving = nextPlayerNumber;

            var lotus = this.get_lotus(this.state.player_moving);
            var lotus_space = this.find_space(lotus.x, lotus.y);
            var enemies = this.get_enemies(lotus_space);
            if(enemies.length > 0) {
                this.state.piece_selected = lotus;
                this.state.locked = true;
                lotus_space.selected = true;
                this.make_moves_selectable();
                var moves = this.board.filter(s => s.selectable);
                if(moves.length === 0) {
                    this.declare_winner(oldPlayerNumber);
                }
            } else {
                this.make_pieces_selectable();
            }
            this.state.moves.push(JSON.parse(JSON.stringify(this.state.current_move)));
            //this.get_next_move().then(this.play_computer_turn);
            this.play_computer_turn;
            this.state.current_move = null;
            //this.state.turn_number++;
        },
        swap_player: function(player_number) {
            return + !player_number;
        },
        declare_winner: function(player_number) {
            var player = this.state.players[player_number];
            console.log(player.name);
            for(var i = 0; i < this.board.length; i++) {
                this.board[i].selectable = false;
            }
            this.winner = player;
        },
        take_pieces: function(piece) {
            if(piece === null) return;
            var enemies = this.get_enemies(this.find_space(piece.x, piece.y));
            var enemies_taken = [];
            for(let i = 0; i < enemies.length; i++) {
                if(this.take_matrix[piece.element].includes(enemies[i].element)) {
                    const space = this.find_space(enemies[i].x, enemies[i].y);
                    space.has_piece = false;
                    space.piece = null;
                    enemies_taken.push(enemies[i]);
                    const index = this.state.pieces.findIndex(p => p === enemies[i]);
                    this.state.pieces.splice(index, 1);
                }
            }
            return enemies_taken;
        },
        has_avatar: function (player_number) {
            var test = this.state.pieces.filter(
                p => p.player_number === player_number && p.element === 'AVATAR'
            );
            return test.length > 0;
        },
        restore_avatar: function() {
            

            for(const player_key in this.state.players) {
                const player_number = parseInt(player_key);
                if(this.has_avatar(player_number)) return;
                const y_pos = player_number === 0 ? 8 : -8;
                const avatar_space = this.find_space(0, y_pos);
                if(avatar_space.has_piece === false) {
                    const avatar = {x: 0,
                                  y: y_pos,
                                  player_number: player_number,
                                  element: 'AVATAR'};
                    avatar_space.piece = avatar;
                    avatar_space.has_piece = true;
                    this.state.pieces.push(avatar);
                    this.add_step(this.move_types.REGENERATE_AVATAR);
                }
            }
        },
        play_computer_turn: function(move) {
            console.log(move);
        },
        select: function(value) {
            value.selected = !value.selected;
            if(value.selected) {
                this.state.piece_selected = value.piece;
                this.make_moves_selectable(value);
            } else {
                this.state.piece_selected = null;
                this.make_pieces_selectable();
            }
        },
        make_moves_selectable: function() {
            for(var i = 0; i < this.board.length; i++) {
                this.board[i].selectable = false;
            }
            var x = this.state.piece_selected.x;
            var y = this.state.piece_selected.y;
            for(let i = 0; i < this.move_matrix.length; i++) {
                const space = this.find_space(x + this.move_matrix[i].x, y + this.move_matrix[i].y);
                if(space == null) continue;
                if(!space.has_piece) {
                    if(this.state.piece_selected.element !== 'LOTUS') {
                        space.selectable = true;
                    } else {
                        if(this.get_enemies(space).length === 0) {
                            space.selectable = true;
                        }
                    }

                } else if(this.state.piece_selected.element !== 'LOTUS'
                          && space.piece.player_number === this.state.player_moving) {
                    const jump_space = this.find_space(
                        space.x + this.move_matrix[i].x, space.y + this.move_matrix[i].y
                    );
                    if(jump_space != null && !jump_space.has_piece) {
                        jump_space.selectable = true;
                    }
                }
            }
        },
        make_pieces_selectable: function() {
            for(var i = 0; i < this.board.length; i++) {
                this.board[i].selectable =
                    (this.board[i].has_piece &&
                    (this.board[i].piece.player_number === this.state.player_moving));
            }
        },
        find_space: function(x, y) {
            return this.board.find(function(el) {
                return el.x === x && el.y === y;
            });
        },
        get_lotus: function(player_number) {
            return this.state.pieces.find(function(el) {
                return el.player_number === player_number && el.element === 'LOTUS';
            });
        },
        push_move_step: function(space, takes) {
            this.state.current_move.move_steps.push(
                {x: space.x, y: space.y, takes: takes.map(t => JSON.parse(JSON.stringify(t)))}
            );
        },
        get_next_move: function() {
            //var dat = JSON.stringify(this.generate_game_object());
//        	console.log(dat);
//        	return $.post(moveUrl, {json: dat}, function(data) {
//        		console.log(data);
//        	}, 'application/json');
//
            console.log(JSON.stringify(this.generate_game_object(), null, 2));

            // return $.ajax({
            //     url: moveUrl,
            //     type: "POST",
            //     data: data,
            //     contentType: "application/json; charset=utf-8",
            //     dataType: "json",
            //     success: function(ret) {
            //         console.log(ret);
            //     }
            // });

            return new Promise().resolve();
        },
        generate_move: function(piece, player_number) {
            //make sure turn number has been initialized
            if(typeof(this.state.turn_number) !== typeof(1)) {
                this.state.turn_number = 0;
            }
            return {
                player_number: player_number,
                move_number: this.state.turn_number++,
                total_steps: 0,
                //copy piece to preserve the initial state of the piece
                //SHOULD we do this? Could skip the 'from' in addStep ...
                piece: this.copy_json(piece),
                steps: [],
//        		addStep: function(move_type, takes, from_x, from_y, to_x, to_y) {
//        			var move = this;
//					move.steps.push({
//						move_type: move_type,
//						step_number: move.total_steps++,
//						takes: takes.map(t => app.copy_json(t)),
//						initial_position: {x: from_x, y: from_y},
//						final_position: {x: to_x, y: to_y}
//					});
//        		}
            }
        },
        //TODO: fix this probably
        generate_game_object: function() {
            return {
                board: {
                    //spaces: this.board,
                    pieces: this.state.pieces
                },
                players: this.state.players,
                player_moving: this.state.player_moving,
                turn_number: this.state.turn_number,
                winner: this.winner,
                moves: this.state.moves,
                current_move: this.state.current_move,
            }
        },
        copy_json: function(obj) {
            return JSON.parse(JSON.stringify(obj))
        }
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.margin-10 {
    margin: 10px;
}
.board-container {
    position: relative;
    width: 720px;
    height: 720px;
    text-align: center;
    background: rgb(70, 133, 68);
    float: left;
}
.background-container {
    position: relative;
    /* margin: auto; */
    display: flex;
    z-index: 0;
    background-image: url("../assets/TransparentBGPaiShoBoard.png");
    width: 720px;
    height: 720px;
    transform: rotate(-45deg);
}
</style>
