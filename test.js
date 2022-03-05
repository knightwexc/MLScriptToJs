console.log("conected to test js")
const documents = [
    {
      id: 1,
      title: 'Moby Dick'
    }
  ]
  
  let miniSearch = new MiniSearch({
    fields: ['title'] 
  })
  
  miniSearch.addAll(documents)
  

  let results = miniSearch.search('moby')
  console.log(results)