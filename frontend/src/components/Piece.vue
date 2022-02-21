<template>
    <div class="fake-border" :class="{'player0' : piece.player_number === 0, 'player1' : piece.player_number === 1}">
        <div :class="classes"></div>
    </div>
</template>

<script>
export default {
    name: 'Piece',
    props: ['piece'],
    computed: {
		classes: function() {
			return "piece " + this.piece.element.toLowerCase();
		}
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.piece {
    border-radius: 50%;
    width: 80%;
    height: 80%;
    margin: 10%;
    opacity: 1;
    /*text-align: center;*/
}

.fake-border {
    border-radius: 50%;
    width: 80%;
    height: 80%;
    margin: 10%;
    opacity: 1;
    display: inline-block;
    text-align: center;
}

.player0 {
    background: black;
}

.player1 {
    background: silver;
}
.piece-enter, .piece-leave {
	opacity: 0;
}
.piece.avatar {
	background: purple;
}

.piece.lotus {
	background: lightsteelblue;
}

.piece.fire {
	background: red;
}

.piece.air {
	background: gold;
}

.piece.earth {
	background: green;
}

.piece.water {
	background: blue;
}
</style>
