<template>
  <div class="standard-button">{{ value }}</div>
</template>

<script>
export default {
  props: ['value'],
  name: "standard-button"
}
</script>

<style lang="scss" scoped>
.standard-button {
  display: flex;
  color: #e5e5e5;
  text-align: center;
  align-items: center;
  justify-content: center;
  word-spacing: 1pt;
  font-size: 9pt;
  user-select: none; /* supported by Chrome and Opera */
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */

  background: #333333;
  border-radius: 5px;
  border-top: 1px solid rgba(41, 41, 41, 0);
  border-right: 1px solid #292929;
  border-bottom: 1px solid #292929;
  border-left: 1px solid rgba(41, 41, 41, 0);
  box-shadow: #8C8C8C -1px -1px 0 1px;
  padding: 7px;
  margin-top: 2px;
  margin-bottom: 1px;

  &:hover {
    background: #414141;
  }

  &:active {
    background: #414141;
    border-radius: 5px;
    border: 1px solid #292929;
    box-shadow: none;
  }
}
</style>