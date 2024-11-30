<template>
  <div
      id="infobox"
      class="info-box">
    <span v-for="(key, index) in Object.keys(details)" :key="index">
      {{ key }}: {{ details[key] }}
    </span>
  </div>
</template>

<script>
export default {
  name: "InfoBox",
  props: ["details"],
  data() {
    return {}
  },
  methods: {}
}
</script>

<style lang="scss" scoped>

.info-box {
  position: relative;
  justify-content: center;
  display: flex;
  flex-direction: column;
  width: max-content;
  height: fit-content;
  border: solid 1px #E5E5E5;
  font-size: 13pt;
  padding: 10px;
  filter: none;
  background: #333333;
  color: #E5E5E5;
}

</style>