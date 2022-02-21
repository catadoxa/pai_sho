<template>
    <div class="top">
        <div>{{player}}'s Turn!</div>
        <button type="button" 
            @click="end" 
            :disabled="endTurnDisabled">End Turn</button>
    </div>
</template>

<script>
export default {
    name: 'GamePanel',
    props: ['endTurnDisabled', 'player'],
    methods: {
        end: function() {
            this.$emit('end-turn');
        }
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    div.top {
        margin: 10px;
        position: relative;
        float: left;
        background-color: rgb(142, 142, 158);
        height: 720px;
        width:150px;
    }
</style>
