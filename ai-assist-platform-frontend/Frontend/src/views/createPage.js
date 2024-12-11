export default function createPage(lsData, nodes, edges, needLayouting, name, router, lsKey) {
    let maxID = 0
    let newAgent = null
    let title = name
    if (lsData) {
        lsData.forEach(agent => {
            if (agent.id > maxID) {
                maxID = agent.id
            }
        });
        newAgent = {
            id: ++maxID,
            title: title,
            to: '/agent_' + maxID,
            nodes: nodes,
            edges: edges,
        }
        lsData.push(newAgent)
        localStorage.setItem(lsKey, JSON.stringify(lsData))
    } else {
        newAgent = {
            id: ++maxID,
            title: title,
            to: '/agent_' + maxID,
            nodes: nodes,
            edges: edges,
        }
        localStorage.setItem(lsKey, JSON.stringify([newAgent]))
    }
    
    router.push({ path: newAgent.to, query: { id: newAgent.id, nodes: newAgent.nodes, edges: newAgent.edges, needLayouting: needLayouting } });
}