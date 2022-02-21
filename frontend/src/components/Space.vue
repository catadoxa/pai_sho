<template>
    <div class="space"
         :style="style"
         @click="parse_click">
        <transition name="piece">
            <Piece :piece="space.piece"
                   v-if="space.has_piece">
            </Piece>
        </transition>
        <div :class="overlay"></div>
    </div>
</template>

<script>
import Piece from './Piece.vue'

export default {
    name: 'Space',
    components: {
        Piece
    },
    props: ['space', 'piece_selected', 'locked'],
    data: function() {
        var l = (340 + 28.2833*this.space.x) + 'px';
        var t = (340 - 28.2833*this.space.y) + 'px';
        return {style: {top: t, left: l}}
    },
    computed: {overlay: function() {
            var classString = 'overlay';
            if(this.space.selectable === true) classString += ' selectable';
            if(this.space.selected === true) classString += ' selected';
            return classString;
        }
    },
    methods: {
        parse_click: function() {
            if(!this.space.selectable && !this.space.selected) return;
            if(this.space.selected && this.locked) return;

            if(this.piece_selected != null && !this.space.selected) {
                this.move();
            } else {
                this.select();
            }
        },
        move: function() {
            this.$emit('move', {move_to: this.space, piece: this.piece_selected})
        },
        select: function() {
            this.$emit('select', this.space);
        }
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.space {
    z-index: 1;
    position: absolute;
    width: 40px;
    height: 40px;
    padding: 0px;
    display: inline-block;
    text-align: center;
}

.overlay {
    opacity: 0.5;
    z-index: 2;
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    border-radius: 50%;
}

.overlay:hover {
    background-color: grey;
}

.overlay.selectable:hover {
    background-color: yellow;
}

.overlay.selected {
    background-color: red;
}

.overlay.selected:hover {
    background-color: DarkOrchid;
}
</style>
