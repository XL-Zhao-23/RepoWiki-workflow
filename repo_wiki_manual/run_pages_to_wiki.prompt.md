请不要清空本总控提示词；只在页面与页面之间隔离页面生成上下文。

````markdown
# 任务：批量执行 pages 提示词并生成 Wiki 文档

你现在是一个代码库 Wiki 文档生成执行器。

请严格按照本总控提示词执行任务。注意：本总控提示词是全局规则，必须在整个任务过程中始终保留，不允许被清空、忽略或覆盖。

## 一、上下文隔离规则

1. 本总控提示词中的规则、输入目录、输出目录、文件命名规则、处理流程，属于全局上下文，必须始终保留。
2. 处理 `pages/` 下每个 `.prompt.md` 文件时，只隔离“页面生成上下文”，不要隔离本总控提示词。
3. 每生成一个页面后，进入下一个页面时，请不要继承上一个页面的正文、结论、模块判断、调用链推断、措辞和不确定项。
4. 当前页面的内容只能基于：
   - 本总控提示词；
   - 当前正在处理的 `.prompt.md` 文件。
5. 禁止把上一个 `.prompt.md` 文件中的代码信息、模块说明、页面结构或生成结果带入当前页面。
6. 如果当前 `.prompt.md` 文件信息不足，请写“需要人工确认”，不要借用其他页面的信息补全。

## 二、输入目录

请处理当前工程目录中的：

```text
pages/
````

其中每个文件都是一个页面生成提示词，例如：

```text
pages/overview.prompt.md
pages/architecture.prompt.md
pages/modules__order.prompt.md
```

## 三、输出目录

请把生成结果保存到：

```text
output/wiki_docs/
```

如果目录不存在，请自动创建。

## 四、文件命名规则

请按照以下规则把 `.prompt.md` 转换成 `.md`：

1. 去掉文件名末尾的 `.prompt.md`
2. 把文件名中的双下划线 `__` 转换为目录分隔符 `/`
3. 最后加上 `.md`
4. 保存到 `output/wiki_docs/`

示例：

```text
pages/overview.prompt.md
→ output/wiki_docs/overview.md

pages/architecture.prompt.md
→ output/wiki_docs/architecture.md

pages/modules__order.prompt.md
→ output/wiki_docs/modules/order.md

pages/modules__cache.prompt.md
→ output/wiki_docs/modules/cache.md
```

## 五、每个文件的处理步骤

请对 `pages/` 下每一个 `.prompt.md` 文件重复执行以下步骤：

### Step 1：读取当前提示词

读取当前 `.prompt.md` 文件的完整内容。

### Step 2：隔离页面上下文

在生成当前页面时，只使用：

```text
本总控提示词 + 当前 .prompt.md 文件内容
```

不要使用上一个页面的正文、结论、模块判断、调用链推断或不确定项。

### Step 3：按照当前提示词生成 Markdown

严格按照当前 `.prompt.md` 中的要求生成 Wiki 页面。

生成内容应满足：

* 面向新接手项目的研发同学；
* 先讲结论，再讲细节；
* 类名、方法名、路径、配置项使用代码格式；
* 能画图的地方使用 Mermaid；
* 不确定的地方写“需要人工确认”；
* 不要输出与当前页面无关的内容；
* 不要编造不存在的类、方法、接口、模块、调用链或业务含义。

### Step 4：保存结果

按照文件命名规则，把生成的 Markdown 保存到 `output/wiki_docs/` 对应路径。

### Step 5：继续下一个文件

完成当前文件后，继续处理下一个 `.prompt.md` 文件，直到 `pages/` 文件夹中的所有提示词全部处理完成。

## 六、完成后输出汇总

全部处理完成后，请输出一个简短汇总，包括：

1. 一共处理了多少个 `.prompt.md` 文件；
2. 生成了哪些 `.md` 文件；
3. 哪些页面存在“需要人工确认”的内容；
4. 是否有文件处理失败，如果有，请说明失败原因。

现在请开始执行。

````