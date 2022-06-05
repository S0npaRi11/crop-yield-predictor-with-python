const stateSelect = document.querySelector('select#state')
const districtSelect = document.querySelector('select#district')
const seasonSelect = document.querySelector('select#season')
const cropSelect = document.querySelector('select#crop')
const yearInput = document.querySelector('input#year')
const areaInput = document.querySelector('input#area')


// populate options function
const populateOptions = (selectRef, data) => {
    data.forEach(d => {
        const option = document.createElement('option')
        option.textContent = d.name
        option.value = d.value

        selectRef.appendChild(option)
    })
}

// sorting function
const sort = (data) => {
    data.sort((a,b) => {
        return (a.value - b.value)
    })
}

sort(STATES)

sort(SEASONS)
// console.log(STATES)

// populate seasons
populateOptions(seasonSelect, SEASONS)

// populate crops
populateOptions(cropSelect, CROPS)

// populate states
populateOptions(stateSelect, STATES)

// populate districts
stateSelect.addEventListener('change', (e) => {

    // clear any previous options
    const previousOptions = districtSelect.options
    Array.from(previousOptions).forEach(p => {
        p.remove()
    })
    const selectedStateValue = e.target.value
    let selectedState
    STATES.forEach(a => {
        if(a.value.toString() === selectedStateValue){
            selectedState = a
        } 
    })

    const districts = selectedState.districts
    sort(districts)
    populateOptions(districtSelect, districts)
})

// registration form

// login form


// prediction form
$(document).ready(() => {
    $('.prediction').hide()
    
    $('#predictionForm').submit((e) => {
        e.preventDefault()

        const formValues = []

        const form = $('form')[0]
        Array.from(form.elements).forEach(f => {
            
            if(f.value !== undefined || f.value !== ''){
                formValues.push(f.value)
            }
        })
             const params = `state=${formValues[0]}&district=${formValues[1]}&year=${formValues[4]}&season=${formValues[2]}&crop=${formValues[3]}&area=${formValues[5]}`
        $.get('runPrediction.php?'+params, (data, status) => {
            result = data
        }).done(() => {
            $('#pred-crop').text(CROPS.find((a) => a.value == formValues[3]).name)
            $('#pred-year').text(formValues[4])
            $('#pred-value').text(Math.round(result))

            $('.prediction').fadeIn()
        })

        console.log('form submitted')
    })
})