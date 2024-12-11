import { useVueFlow } from '@vue-flow/core'
import { ref, watch } from 'vue'

/**
 * In a real world scenario you'd want to avoid creating refs in a global scope like this as they might not be cleaned up properly.
 * @type {{draggedType: Ref<string|null>, isDragOver: Ref<boolean>, isDragging: Ref<boolean>}}
 */
const state = {
  /**
   * The type of the node being dragged.
   */
  draggedType: ref(null),
  isDragOver: ref(false),
  isDragging: ref(false),
}

export default function useDragAndDrop() {
  const { draggedType, isDragOver, isDragging } = state

  const { addNodes, screenToFlowCoordinate, onNodesInitialized, updateNode, getNodes } = useVueFlow()

  watch(isDragging, (dragging) => {
    document.body.style.userSelect = dragging ? 'none' : ''
  })

  function onDragStart(event, type) {
    if (event.dataTransfer) {
    
        event.dataTransfer.setData('application/vueflow', type)
        event.dataTransfer.effectAllowed = 'move'
    }

    draggedType.value = type
    isDragging.value = true

    document.addEventListener('drop', onDragEnd)
  }

  /**
   * @returns {string} - A unique id.
   */
  function getId() {
    let id = 0;

    if (getNodes && Array.isArray(getNodes.value)) {
      getNodes.value.forEach(node => {
        let nodeID = Number(node.id.split('n')[1])
        if (id < nodeID) {
          id = nodeID
        }
      })
    }

    return `n${++id}`
  }

  /**
   * Handles the drag over event.
   *
   * @param {DragEvent} event
   */
  function onDragOver(event) {
    event.preventDefault()

    if (draggedType.value) {
      isDragOver.value = true

      if (event.dataTransfer) {
        event.dataTransfer.dropEffect = 'move'
      }
    }
  }

  function onDragLeave() {
    isDragOver.value = false
  }

  function onDragEnd() {
    isDragging.value = false
    isDragOver.value = false
    draggedType.value = null
    document.removeEventListener('drop', onDragEnd)
  }

  /**
   * Handles the drop event.
   *
   * @param {DragEvent} event
   */
  function onDrop(event) {
    const position = screenToFlowCoordinate({
      x: event.clientX,
      y: event.clientY,
    })

    const nodeId = getId()
    
    let myMeta = {}
    let NodeInfo = {}
    if (draggedType.value === 'custom') {
      myMeta = {source1ID : crypto.randomUUID(), source2ID: crypto.randomUUID()}
    } else if (draggedType.value === 'operator') {
      myMeta = {source1ID : crypto.randomUUID(), target1ID: crypto.randomUUID(), target2ID: crypto.randomUUID()}
    } else if (draggedType.value === 'result') {
      myMeta = {target1ID : crypto.randomUUID()}
    } else if (draggedType.value === 'prompt') {
      NodeInfo.template = ref('')
      NodeInfo.prompt_values = ref({})
      myMeta = {sourceOutputID : crypto.randomUUID()}
    } else if (draggedType.value === 'model') {
      NodeInfo.api_key = ref('')
      NodeInfo.model_name = ref('')
      NodeInfo.temperature = ref(1)
      NodeInfo.top_p = ref(1)
      NodeInfo.max_tokens = ref(5000)
      NodeInfo.stop_seq = ref('')
      NodeInfo.freq_penalty = ref(0)
      NodeInfo.pres_penalty = ref(0)
      myMeta = {sourceOutputID : crypto.randomUUID()}
    } else if (draggedType.value === 'chain') {
      myMeta = {
        sourceOutputID : crypto.randomUUID(), 
        targetModelID: crypto.randomUUID(),
        targetPromptID: crypto.randomUUID(),
        targetToolsID: crypto.randomUUID(),}
    } else if (draggedType.value === 'var') {
      NodeInfo.var = ref('')
      myMeta = {
        sourceOutputID : crypto.randomUUID(),}
    } else if (draggedType.value === 'visual') {
      NodeInfo.text_to_visual = ref('')
      myMeta = {
        targetInputID : crypto.randomUUID(),}
    } else if (draggedType.value === 'websearch') {
      NodeInfo.api_key = ref('')
      myMeta = {
        sourceOutputID : crypto.randomUUID(),}
    }

    const newNode = {
      id: nodeId,
      type: draggedType.value,
      position,
      data: { meta: myMeta, ...NodeInfo },
    }

    /**
     * Align node position after drop, so it's centered to the mouse
     *
     * We can hook into events even in a callback, and we can remove the event listener after it's been called.
     */
    const { off } = onNodesInitialized(() => {
      updateNode(nodeId, (node) => ({
        position: { x: node.position.x - node.dimensions.width / 2, y: node.position.y - node.dimensions.height / 2 },
      }))

      off()
    })

    addNodes(newNode)
  }

  return {
    draggedType,
    isDragOver,
    isDragging,
    onDragStart,
    onDragLeave,
    onDragOver,
    onDrop,
  }
}
const testText2 = `Формула Лагранжа, также известная как интерполяционная формула Лагранжа, используется для нахождения многочлена, который проходит через заданные точки. Если у вас есть \( n + 1 \) точек \((x_0, y_0), (x_1, y_1), \ldots, (x_n, y_n)\), то интерполяционный многочлен \( P(x) \) можно записать в следующем виде:

$$
P(x) = \sum_{i=0}^{n} y_i L_i(x)
$$


где \( L_i(x) \) — это базисные полиномы Лагранжа и определяются как:

$$
L_i(x) = \prod_{\substack{0 \leq j \leq n \\ j \neq i}} \frac{x - x_j}{x_i - x_j}
$$

$$
L_i(x) = \prod_{\substack{0 \leq j \leq n \\ j \neq i}} \frac{x - x_j}{x_i - x_j}
$$

Каждый из этих полиномов \( L_i(x) \) равен 1 в точке \( x = x_i \) и равен 0 в остальных узлах.

Таким образом, формула Лагранжа позволяет вам построить многочлен степени не выше \( n \), который точно проходит через все заданные точки.

`
const testText = `# Заголовок 1
## Заголовок 2
### Заголовок 3

Это абзац текста с **жирным текстом** и *курсивным текстом*.

- Пункт списка 1
- Пункт списка 2
  - Вложенный пункт 2.1
  - Вложенный пункт 2.2

1. Нумерованный пункт 1
2. Нумерованный пункт 2

[Ссылка на Google](https://www.google.com)

\`\`\`javascript
console.log('Пример кода JavaScript');
\`\`\`

<img src="data:image/gif;base64,R0lGODlhEAAOALMAAOazToeHh0tLS/7LZv/0jvb29t/f3//Ub//ge8WSLf/rhf/3kdbW1mxsbP//mf///yH5BAAAAAAALAAAAAAQAA4AAARe8L1Ekyky67QZ1hLnjM5UUde0ECwLJoExKcppV0aCcGCmTIHEIUEqjgaORCMxIC6e0CcguWw6aFjsVMkkIr7g77ZKPJjPZqIyd7sJAgVGoEGv2xsBxqNgYPj/gAwXEQA7" width="16" height="14" alt="иконка папки"/>

> Цитата

| Syntax    | Description |
| --------- | ----------- |
| Header    | Title       |
| Paragraph | Text        |

\`\`\`mermaid
graph TD;
  A-->B;
  A-->C;
  B-->D;
  C-->D;
\`\`\`

# Заголовок 1
## Заголовок 2
### Заголовок 3

Это абзац текста с **жирным текстом** и *курсивным текстом*.

- Пункт списка 1
- Пункт списка 2
  - Вложенный пункт 2.1
  - Вложенный пункт 2.2

1. Нумерованный пункт 1
2. Нумерованный пункт 2

\`\`\`mermaid
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Hello John, how are you?
    loop HealthCheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts <br/>prevail!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!
\`\`\``