document.addEventListener('DOMContentLoaded', ()=>{
  const form = document.getElementById('quiz')
  const questionsContainer = document.getElementById('questions')
  const submitBtn = document.getElementById('submitBtn')
  const resetBtn = document.getElementById('resetBtn')
  const reshuffleBtn = document.getElementById('reshuffleBtn')
  const resultSection = document.getElementById('result')
  const scoreText = document.getElementById('scoreText')
  const advice = document.getElementById('advice')

  const POOL_SIZE = 200
  const SHOW_N = 5

  // 生成题库（示例占位）。你可以把中文题目替换到这里的数组中。
  const questionPool = Array.from({length:POOL_SIZE}, (_,i)=>({
    id: i+1,
    text: `问题 ${i+1}：这是题库中的占位题目。请替换为真实题目文本。`
  }))

  let currentSet = []

  function pickRandomN(n){
    const indices = Array.from({length:questionPool.length}, (_,i)=>i)
    // Fisher-Yates shuffle partial
    for(let i=indices.length-1;i>0 && indices.length - i <= n*5;i--){
      const j = Math.floor(Math.random()*(i+1))
      ;[indices[i], indices[j]] = [indices[j], indices[i]]
    }
    // take first n unique
    return indices.slice(0,n).map(i=>questionPool[i])
  }

  function renderQuestions(){
    questionsContainer.innerHTML = ''
    currentSet = pickRandomN(SHOW_N)
    currentSet.forEach((q, idx)=>{
      const div = document.createElement('div')
      div.className = 'question'
      div.dataset.qid = q.id
      div.innerHTML = `<p class="q-text">${idx+1}. ${q.text}</p>
        <label><input type="radio" name="q${idx+1}" value="3"> 非常符合</label>
        <label><input type="radio" name="q${idx+1}" value="2"> 比较符合</label>
        <label><input type="radio" name="q${idx+1}" value="1"> 有些符合</label>
        <label><input type="radio" name="q${idx+1}" value="0"> 不符合</label>`
      questionsContainer.appendChild(div)
    })
    updateSubmitState()
  }

  function updateSubmitState(){
    let answered = 0
    for(let i=1;i<=SHOW_N;i++){
      if(form.querySelector(`input[name=q${i}]:checked`)) answered++
    }
    submitBtn.disabled = answered !== SHOW_N
  }

  form.addEventListener('change', updateSubmitState)

  form.addEventListener('submit', e=>{
    e.preventDefault()
    let total = 0
    for(let i=1;i<=SHOW_N;i++){
      const el = form.querySelector(`input[name=q${i}]:checked`)
      if(el) total += Number(el.value)
    }

    const max = SHOW_N*3
    let level = ''
    let detail = ''
    const pct = total / max
    if(pct <= 0.33){
      level = '低'
      detail = '你的回答总体偏向平稳，当前压力或焦虑水平较低。'
    } else if(pct <= 0.66){
      level = '中等'
      detail = '你的回答显示一定的压力或焦虑，建议注意放松与休息。'
    } else {
      level = '较高'
      detail = '你的压力或焦虑水平较高，建议考虑寻求专业帮助。'
    }

    scoreText.textContent = `得分：${total}/${max} （${level}）`
    advice.textContent = detail
    resultSection.classList.remove('hidden')
    resultSection.scrollIntoView({behavior:'smooth'})
  })

  resetBtn.addEventListener('click', ()=>{
    form.reset()
    submitBtn.disabled = true
    resultSection.classList.add('hidden')
    scoreText.textContent = ''
    advice.textContent = ''
  })

  reshuffleBtn.addEventListener('click', ()=>{
    form.reset()
    resultSection.classList.add('hidden')
    scoreText.textContent = ''
    advice.textContent = ''
    renderQuestions()
  })

  // 首次渲染
  renderQuestions()
})
