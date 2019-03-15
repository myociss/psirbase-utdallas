$(document).ready(function(){
   
    var selectedSpecies = $('.icon-inner-column')[0];
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
        $('input#q').attr('placeholder', 'Enter ' + searchType);
        $('input#search-type').val(searchType);
    })

})