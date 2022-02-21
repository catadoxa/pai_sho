<template>
    <div>
        {{ winner.name }} wins!
    </div>
</template>

<script>
export default {
    name: 'Winner',
    props: ['winner'],
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div {
    position: relative;
    background: black;
    color: red;
    z-index: 2;
}
</style>
