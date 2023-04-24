
const _mainAppend = function(element){
    const main = document.querySelector('main');
    main.appendChild(element);
    return
};

const _checkInputChoice = function(input){
    const error = new Error('input choice is null');
    if(!input){
        throw error
    }
};

const _checkParams = function(params){
    const error = new Error('params are null');
    if(!params){
        throw error
    }
};

const _createContentContainer = function(){
    const container = document.createElement('section');
    container.classList.add('container');
    return container
}

const _getFormId = function(){
    const allForms = Array.from(document.querySelectorAll('form'));
    const targetForm = allForms.filter((form )=> !form.closest('section').classList.contains('invisible'))[0]
    return  targetForm ? targetForm.id : ''
};


const _removeCurrentRendering = function(){
    const container = document.querySelector('.container');
    return container ? container.remove() : null
};

const formMapGenerator = function(){
    
    const _checkTrue = function(value){
        return !!value

    };

    const _joinParams = function(values){
        const joined = values.join('&')
        return joined
    };

    const user_repo_url = function(){
        const usernameInput = document.querySelector('input[name="user_repo_username"]');
        const limitInput = document.querySelector('input[name="user_repo_limit"]');
        const inputs = [usernameInput,limitInput];
        const values = inputs.every((input)=> _checkTrue(input)) ? [`username=${usernameInput.value}`,`limit=${limitInput.value}`]: null;
        const urlparams = values.every((value) => _checkTrue(value)) ? _joinParams(values) : values;        
        return urlparams
    };

    const formToUrl = new Map();
    formToUrl.set('user_repo', user_repo_url);
    return formToUrl
};

const retrieveData = async function(event, link){
    try{
        const formMap = formMapGenerator();
        const inputChoice = event.target.action ? event.target.id : _getFormId();
        const generateParams = formMap.get(inputChoice);
        const params = generateParams();
        _checkInputChoice(inputChoice);
        _checkParams(params);
        const abort = new AbortController()
        currentAbort = abort
        const abortSignal = abort.signal
        const encodedLink = encodeURIComponent(link)
        const urlToUse = link ? `/${inputChoice}?${params}&link=${encodedLink}` : `/${inputChoice}?${params}`
        const req = new Request(urlToUse, {mode:'cors', signal: abortSignal})
        const response = await fetch(req) 
        const userData = await response.json()
        return userData
    }
    catch(error){
        let e = error
        if(e.message === 'The operation was aborted. '){
            return
        }
        else{
            console.log(error)
        }
        return
    }
};

const addEnd = function(){
    const container = document.querySelector('.container');
    const endContainer = document.createElement('div');
    container.appendChild(endContainer);
    const endMessage = document.createElement('p');
    endMessage.textContent = 'END';
    endContainer.appendChild(endMessage);
    return
}

const addLoadingSpinner = function(){
    _removeCurrentRendering();
    const container = _createContentContainer();
    _mainAppend(container);
    
    const spinner = document.createElement('div');
    spinner.classList.add('spin');
    container.appendChild(spinner);
}

const addPagination = function(links){
    const checkIfLinks = function(){
        return Object.keys(links).length
    };

    const checkLink = function(linkId,nav){
        return links[linkId] ? effectLink(linkId,nav) : effectPlaceholder(linkId,nav)
    };

    const checkIfLast = function(){
        const last = document.querySelector('#last');
        return last.classList.contains('placeholder') ? addEnd() : false
    };

    const effectLink = function(linkId,nav){
        const button = document.createElement('button');
        button.classList.add('page-nav');
        button.id = linkId;
        button.textContent = linkId;
        nav.appendChild(button);
        return button

    };

    const effectPlaceholder = function(linkId, nav){
        const button = document.createElement('button');
        button.classList.add('placeholder');
        button.id = linkId;
        button.textContent = linkId;
        button.disabled = true;
        nav.appendChild(button);
        return button
    };

    const effectRenderPagination = function(){
        const linkIds = ['first', 'prev', 'next', 'last'];
        const container = document.querySelector('.container');
        const pageNavContainer = document.createElement('nav');
        pageNavContainer.addEventListener('click', navigateToNewPage);
        container.appendChild(pageNavContainer);
        const buttons = linkIds.map((id) => checkLink(id,pageNavContainer));
        checkIfLast();
        return pageNavContainer

    };

    const navigateToNewPage = function(event){
        return guardPageNav(event,links)
    };

    return checkIfLinks ? effectRenderPagination() : false;

};

const renderTree = function(body){
    _removeCurrentRendering();
    const container = _createContentContainer();
    _mainAppend(container);

    const parseSingleItem = function(item,treeContainer){

//At the moment, this is tightly coupled to the API's current data
//structure. This shall be updated to incorporate Breadth First Search.
        const parseItemStructure = function(itm,container,integrators){
            
            const {integrateKey, integrateValue} = integrators;

            let currentContainer = container;
            let parent = itm
            let check
            
            
            const checkValue = function(value){
                const checkNull = value === null || value === undefined;
                const checkArray = Array.isArray(value) 
                const checkString = typeof value === 'string'; 
                const checkNumber = typeof value === 'number'; 
                return checkNull || checkArray || checkString || checkNumber 
            };

            while(!check){
                const finaliseOperation = function(){
                    integrateValue(parent[key],currentContainer);
                    check = true
                }

                const key = Object.keys(parent)[0];
                currentContainer = integrateKey(key,currentContainer);
                checkValue(parent[key]) ? finaliseOperation(): parent = parent[key];
            };

            const entries = Object.entries(parent).slice(1);
            const integrateRemainingValue = function(entries){
                const [key,value] = entries;
                const details = integrateKey(key,currentContainer);
                integrateValue(value,details)
            };
            entries.map(integrateRemainingValue);

        };
        
        const integrateKey = function(key, liCont){
            const ul = document.createElement('ul');
            const li = document.createElement('li');
            const details = document.createElement('details');

            if(liCont.classList.contains('tree_branch')){
                liCont.appendChild(details)
            }
            else{
                liCont.appendChild(ul)
                ul.appendChild(li);
                li.appendChild(details)
            }

           

            details.setAttribute('open','true');
            const summary = document.createElement('summary');
            summary.textContent = key
            details.appendChild(summary);
            return details;
        };

        //Of course the following does not take into account
        //if value is array of objects. Present version of
        //API has no such structure but something to watch
        //out for.

        const integrateValue = function(value,details){

            const ul = document.createElement('ul');
            details.appendChild(ul);

            const integrateUnit = function(unit){
                const li = document.createElement('li');
                li.textContent = unit ?? 'null';
                ul.appendChild(li);
            };
            
            Array.isArray(value) ? value.map(integrateUnit) : integrateUnit(value)
            return ul
        };
    
        const integrators = {integrateKey, integrateValue};
        parseItemStructure(item,treeContainer,integrators);
    }

    const tree = document.createElement('ul');
    tree.classList.add('tree');
    container.appendChild(tree);
    const listContainer = document.createElement('li');
    listContainer.classList.add('tree_branch');
    tree.appendChild(listContainer)
    body.map((item) => parseSingleItem(item,listContainer))
   
};

const renderError = function(response){
    
    const effectRenderError = function(){
        _removeCurrentRendering();
        const container = _createContentContainer();
        _mainAppend(container);

        const newError = document.createElement('div');
        newError.classList.add('error');
        container.appendChild(newError);

        const errorMessage = document.createElement('p');
        errorMessage.textContent = response.error;
        newError.appendChild(errorMessage)
        console.log(response.response) //log response. 

        return newError
    };

    return response.error ? effectRenderError() : null  
};

const effectRequest = async function(event, link){
    addLoadingSpinner();
    const data = await retrieveData(event,link)
    const renderType = renderError(data) ? 'error' : renderTree(data.body);
    const pagination = data.links ? addPagination(data.links) : addEnd();

};

const guardFormRequest = async function(event){
    const effectFormRequest = async function(){
        event.preventDefault();
        return await effectRequest(event)
    };
    return event.target.action ? await effectFormRequest(event) : false
};

const guardPageNav = async function(event,links){
    if(event.target.classList.contains('page-nav')){
        const link = links[event.target.id].url;
        return await effectRequest(event,link)
    } 
};


const selectVisibleForm = function(event){

    const toggleVisible = function(element){
        element.classList.toggle('invisible',false);
    };

    const toggleInvisible = function(element){
        element.classList.toggle('invisible',true);
    };

    const mapOptionToFormSection = function(option){
        const value = option.value;
        const section = document.querySelector(`.${value}`);
        return section
    };

    const updateVisibilityStatus = function(option){
        const section = mapOptionToFormSection(option);
        const select = event.currentTarget;
        const selected = select[select.selectedIndex];

        return option === selected ? toggleVisible(section) : toggleInvisible(section);
    };


    const options = Array.from(document.querySelectorAll('option'));
    const availableOptions = options.filter(option => mapOptionToFormSection(option));
    availableOptions.map(updateVisibilityStatus);    
};

const toggleFormEvents = function(){

    const toggleEventOff = function(element){
        element.removeEventListener('submit', guardFormRequest)
    };

    const toggleEventOn = function(element){
        element.addEventListener('submit', guardFormRequest)

    };

    const formVisibilityFilter = function(element){
         return element.closest('section').classList.contains('invisible') ? false : element
    };

    const formInvisibilityFilter = function(element){
        return element.closest('section').classList.contains('invisible') ? element : false
    };

    const allForms = Array.from(document.querySelectorAll('form'));
    const visibleForms = allForms.filter(formVisibilityFilter);
    const invisibleForms = allForms.filter(formInvisibilityFilter);
    visibleForms.map(toggleEventOn);
    invisibleForms.map(toggleEventOff);

};

const addListeners = function(){

    const select = document.querySelector('select');
    if(select){
        select.addEventListener('change',selectVisibleForm);
        select.addEventListener('change',toggleFormEvents);
    }
    
};

addListeners();

//temporary
if(document.querySelector('select')){
   const temporaryDisclosure = document.createElement("div");
   temporaryDisclosure.textContent = 'This page is still in development. Please select "target\'s repositories" to see it in effect.'
   temporaryDisclosure.style.color = 'red';
   temporaryDisclosure.style.fontSize = 'small';
   const select = document.querySelector('select');
   const parent = select.parentElement;
   parent.insertBefore(temporaryDisclosure,select);
}

