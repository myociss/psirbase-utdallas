$(document).ready(function(){
    var groupCount = $('.species-group').length;
    var currentGroupIdx = 0;

    var currentSpeciesGroup = $('.species-group')[currentGroupIdx];

    $.each($('.species-group'), function(i, e){
        if (i != currentGroupIdx){
            $(e).hide();
        }
    })

    //$(currentSpeciesGroup).removeClass('unselected-group');

    setArrows();

    $('.arrow-icon').click(function(){
        //$(currentSpeciesGroup).hide('slide', { direction: 'left' }, 1000);
        if (!$(this).hasClass('disabled')){
            if ($(this).hasClass('arrow-right')){
                //currentGroupIdx++;
                exchangeSpeciesGroups('left', 'right', 1)
            } else {
                //currentGroupIdx--;
                exchangeSpeciesGroups('right', 'left', -1)
            }
            setArrows();
        }
    })

    var selectedSpecies = $(currentSpeciesGroup).find('.icon-inner-column')[0];
    $(selectedSpecies).addClass('selected-species');

    $('.icon-inner-column').click(function(){
        $(this).addClass('selected-species');
        $(selectedSpecies).removeClass('selected-species');
        selectedSpecies = $(this);
        $('input#species-id').val($(this).attr('data-species-id'));
    })

    var selectedSearchType = $('.search-types').find('.selected')[0];

    $('.search-type').click(function(){
        $(this).addClass('selected');
        $(selectedSearchType).removeClass('selected');
        selectedSearchType = $(this);
        var searchType = selectedSearchType.attr('data-search-type');
        $('input#sequence').attr('placeholder', 'Enter ' + searchType);
        $('input#search-type').val(searchType);
    })

    function exchangeSpeciesGroups(direction, opposite, increment){
        $(currentSpeciesGroup).hide('slide', { direction: direction }, 800);
        currentGroupIdx += increment;
        currentSpeciesGroup = $('.species-group')[currentGroupIdx];
        $(currentSpeciesGroup).delay(1000).show('slide', { direction: opposite }, 800);
    }

    function setArrows(){
        if (currentGroupIdx == 0){
            $('.arrow-left').removeClass('arrow-icon-enabled');
        } else {
            $('.arrow-left').addClass('arrow-icon-enabled');
        }

        if (currentGroupIdx == groupCount - 1){
            $('.arrow-right').removeClass('arrow-icon-enabled');
        } else {
            $('.arrow-right').addClass('arrow-icon-enabled');
        }
    }
})