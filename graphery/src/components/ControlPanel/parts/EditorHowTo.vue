<template>
  <q-card>
    <q-card-section>
      How To
      <q-btn
        color="grey"
        round
        flat
        dense
        :icon="expanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
        @click="expanded = !expanded"
      />
    </q-card-section>
    <q-slide-transition>
      <div v-show="expanded">
        <q-separator />
        <q-card-section>
          <MarkdownSection :input-html="html" />
        </q-card-section>
      </div>
    </q-slide-transition>
  </q-card>
</template>
<script>
  import MarkdownSection from '@/components/framework/MarkdownSection';
  export default {
    components: { MarkdownSection },
    data() {
      return {
        html:
          '<table> <thead> <tr> <th>key</th> <th style="text-align:center">keycode</th> <th style="text-align:center">功能</th> </tr> </thead> <tbody> <tr> <td>F8</td> <td style="text-align:center">119</td> <td style="text-align:center">开启/关闭导航</td> </tr> <tr> <td>F9</td> <td style="text-align:center">120</td> <td style="text-align:center">预览/编辑切换</td> </tr> <tr> <td>F10</td> <td style="text-align:center">121</td> <td style="text-align:center">开启/关闭全屏</td> </tr> <tr> <td>F11</td> <td style="text-align:center">122</td> <td style="text-align:center">开启/关闭阅读模式</td> </tr> <tr> <td>F12</td> <td style="text-align:center">123</td> <td style="text-align:center">单栏/双栏切换</td> </tr> <tr> <td>TAB</td> <td style="text-align:center">9</td> <td style="text-align:center">缩进</td> </tr> <tr> <td>CTRL + S</td> <td style="text-align:center">17 + 83</td> <td style="text-align:center">触发保存</td> </tr> <tr> <td>CTRL + D</td> <td style="text-align:center">17 + 68</td> <td style="text-align:center">删除选中行</td> </tr> <tr> <td>CTRL + Z</td> <td style="text-align:center">17 + 90</td> <td style="text-align:center">上一步</td> </tr> <tr> <td>CTRL + Y</td> <td style="text-align:center">17 + 89</td> <td style="text-align:center">下一步</td> </tr> <tr> <td>CTRL + BreakSpace</td> <td style="text-align:center">17 + 8</td> <td style="text-align:center">清空编辑</td> </tr> <tr> <td>CTRL + B</td> <td style="text-align:center">17 + 66</td> <td style="text-align:center"><strong>加粗</strong></td> </tr> <tr> <td>CTRL + I</td> <td style="text-align:center">17 + 73</td> <td style="text-align:center"><em>斜体</em></td> </tr> <tr> <td>CTRL + H</td> <td style="text-align:center">17 + 72</td> <td style="text-align:center"># 标题</td> </tr> <tr> <td>CTRL + 1</td> <td style="text-align:center">17 + 97 or 49</td> <td style="text-align:center"># 标题</td> </tr> <tr> <td>CTRL + 2</td> <td style="text-align:center">17 + 98 or 50</td> <td style="text-align:center">## 标题</td> </tr> <tr> <td>CTRL + 3</td> <td style="text-align:center">17 + 99 or 51</td> <td style="text-align:center">### 标题</td> </tr> <tr> <td>CTRL + 4</td> <td style="text-align:center">17 + 100 or 52</td> <td style="text-align:center">#### 标题</td> </tr> <tr> <td>CTRL + 5</td> <td style="text-align:center">17 + 101 or 53</td> <td style="text-align:center">##### 标题</td> </tr> <tr> <td>CTRL + 6</td> <td style="text-align:center">17 + 102 or 54</td> <td style="text-align:center">###### 标题</td> </tr> <tr> <td>CTRL + U</td> <td style="text-align:center">17 + 85</td> <td style="text-align:center"><ins>下划线</ins></td> </tr> <tr> <td>CTRL + M</td> <td style="text-align:center">17 + 77</td> <td style="text-align:center"><mark>标记</mark></td> </tr> <tr> <td>CTRL + Q</td> <td style="text-align:center">17 + 81</td> <td style="text-align:center">&gt; 引用</td> </tr> <tr> <td>CTRL + O</td> <td style="text-align:center">17 + 79</td> <td style="text-align:center">1. 有序列表</td> </tr> <tr> <td>CTRL + L</td> <td style="text-align:center">17 + 76</td> <td style="text-align:center"><a href="" target="_blank">链接</a></td> </tr> <tr> <td>CTRL + ALT + S</td> <td style="text-align:center">17 + 18 + 83</td> <td style="text-align:center"><sup>上角标</sup></td> </tr> <tr> <td>CTRL + ALT + U</td> <td style="text-align:center">17 + 18 + 85</td> <td style="text-align:center">- 无序列表</td> </tr> <tr> <td>CTRL + ALT + C</td> <td style="text-align:center">17 + 18 + 67</td> <td style="text-align:center">``` 代码块</td> </tr> <tr> <td>CTRL + ALT + L</td> <td style="text-align:center">17 + 18 + 76</td> <td style="text-align:center"><img src="" alt="图片链接" /></td> </tr> <tr> <td>CTRL + ALT + T</td> <td style="text-align:center">17 + 18 + 84</td> <td style="text-align:center">表格</td> </tr> <tr> <td>CTRL + SHIFT + S</td> <td style="text-align:center">17 + 16 + 83</td> <td style="text-align:center"><sub>下角标</sub></td> </tr> <tr> <td>CTRL + SHIFT + D</td> <td style="text-align:center">17 + 16 + 68</td> <td style="text-align:center"><s>中划线</s></td> </tr> <tr> <td>CTRL + SHIFT + C</td> <td style="text-align:center">17 + 16 + 67</td> <td style="text-align:center">居中</td> </tr> <tr> <td>CTRL + SHIFT + L</td> <td style="text-align:center">17 + 16 + 76</td> <td style="text-align:center">居左</td> </tr> <tr> <td>CTRL + SHIFT + R</td> <td style="text-align:center">17 + 16 + 82</td> <td style="text-align:center">居右</td> </tr> <tr> <td>SHIFT + TAB</td> <td style="text-align:center">16 + 9</td> <td style="text-align:center">取消缩进</td> </tr> </tbody> </table>',
        expanded: false,
      };
    },
  };
</script>
