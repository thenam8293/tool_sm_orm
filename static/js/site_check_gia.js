        
            $("#div_dropdown_tho_cu").click(function() {
                $("#div_dropdown_tho_cu").addClass("current_active")
                $("#div_dropdown_can_ho").removeClass("current_active")
                $("#div_dropdown_biet_thu").removeClass("current_active")

                $("#div_main_tho_cu").css("display","")
                $("#div_main_Can_ho").css("display","none")
                $("#div_main_Biet_thu").css("display","none")
            })
            $("#div_dropdown_can_ho").click(function() {
                $("#div_dropdown_tho_cu").removeClass("current_active")
                $("#div_dropdown_can_ho").addClass("current_active")
                $("#div_dropdown_biet_thu").removeClass("current_active")

                $("#div_main_tho_cu").css("display","none")
                $("#div_main_Can_ho").css("display","")
                $("#div_main_Biet_thu").css("display","none")
            })
            $("#div_dropdown_biet_thu").click(function() {
                $("#div_dropdown_tho_cu").removeClass("current_active")
                $("#div_dropdown_can_ho").removeClass("current_active")
                $("#div_dropdown_biet_thu").addClass("current_active")
                
                $("#div_main_tho_cu").css("display","none")
                $("#div_main_Can_ho").css("display","none")
                $("#div_main_Biet_thu").css("display","")
            })

       
        // DOT NUMBER 
        
            function reverseNumber(input) {
                return [].map.call(input, function(x) {
                    return x;
                }).reverse().join(''); 
            };
              
            function plainNumber(number) {
                return number.split(',').join('');
            };
              
            function splitInDots(input) {
                var value = input.value;
                if(isNaN(value.replace(/\,/g,'')) == false) {
                    var plain = plainNumber(value)
                    var reversed = reverseNumber(plain)
                    var reversedWithDots = reversed.match(/.{1,3}/g).join(',')
                    var normal = reverseNumber(reversedWithDots);
                    input.value = normal;
                }else {
                    input.value = ''
                }       
            };
            function dot_number(number) {
                number = String(number).split("").reverse().join("")
                number = number.match(/.{1,3}/g).join(',')
                number = reverseNumber(number)
                return number
            }
        
        // CHECK GIA UY BAN + TT QUY HOACH 
        
        // GET GIA + TT QUY HOACH AJAX
            $(document).on('change','[id^="vi_tri_bds_"]', function() {
                let vi_tri_bds_id = $(this).attr("id")
                let tinh_thanh_id = `tinh_thanh_${vi_tri_bds_id.split("vi_tri_bds_")[1]}`
                let quan_huyen_id = `quan_huyen_${vi_tri_bds_id.split("vi_tri_bds_")[1]}`
                let ten_duong_id = `ten_duong_${vi_tri_bds_id.split("vi_tri_bds_")[1]}`
                let tuyen_duong_id = `tuyen_duong_${vi_tri_bds_id.split("vi_tri_bds_")[1]}`

                $.getJSON($SCRIPT_ROOT + '/ajax_get_gia_uy_ban', {
                    tinh_thanh: $(`#${tinh_thanh_id}`).val(),
                    quan_huyen: $(`#${quan_huyen_id}`).val(),
                    ten_duong: $(`#${ten_duong_id}`).val(),
                    tuyen_duong: $(`#${tuyen_duong_id}`).val(),       
                    vi_tri_bds: $(this).val(),

                }, function(data) {                    
                    if(vi_tri_bds_id.split("vi_tri_bds_")[1] == 'tt_quy_hoach') {
                        $("#result_quy_hoach").css("display", "")

                        let tt_qh = ''
                        $.each(String(data.result[0][0]).split("|"), function(i, r) {
                            tt_qh += `<div style="margin-left: 10px;">${r}</div>`
                        })                       


                        $(`#gia_tri_tai_san_${vi_tri_bds_id.split("vi_tri_bds_")[1]}`).html(tt_qh)
                    }
                    
                  });
                  return false;
            })
        
        // CHECK VI TRI 
        
            var list_vi_tri = ['Vị trí 1',
                'Vị trí 2',
                'Vị trí 3',
                'Vị trí 4'
                ]
            $("#vi_tri_bds_thi_truong").change(function() {
                // TOGGLE 
                if(list_vi_tri.indexOf($(this).val()) != -1 && $(this).val() != 'Vị trí 1' ){
                    $("#div_do_rong_ngo_thi_truong").css("display","")
                    $("#div_kcach_truc_chinh_thi_truong").css("display","")
                }
                else{
                    $("#div_do_rong_ngo_thi_truong").css("display","none")
                    $("#div_kcach_truc_chinh_thi_truong").css("display","none")
                }
                // EMPTY FIELD
                empty_field()
                // AJAX
                $.getJSON($SCRIPT_ROOT + '/ajax_get_dac_diem_vi_tri', {
                    tinh_thanh: $(`#tinh_thanh_thi_truong`).val(),
                    vi_tri: $(this).val(),

                }, function(data) {
                    console.log(data.loi_the)
                    $("#div_select_loi_the").empty()
                    $("#div_select_bat_loi").empty()
                    $.each(data.loi_the, function(i,r) {
                        $("#div_select_loi_the").append(`
                                    <div class="inline_modal_3 float-label-control">                        
                                        <input type="checkbox" id="check_box_loi_the${i}" value="${r}">
                                        <label style="word-wrap: normal; word-break: break-word;width: 90%;vertical-align: top" for="check_box_loi_the${i}">${r}</label>                        
                                    </div>`)
                    })
                    $.each(data.bat_loi, function(i,r) {
                        $("#div_select_bat_loi").append(`
                            <div class="inline_modal_3 float-label-control">                        
                                <input type="checkbox" id="check_box_bat_loi${i}" value="${r}">
                                <label style="word-wrap: normal; word-break: break-word;width: 90%;vertical-align: top" for="check_box_bat_loi${i}">${r}</label>                        
                            </div>`)
                    })
                    // ICHECKBOX
                    $('[id^="check_box_"]').iCheck({
                        checkboxClass: 'icheckbox_square-green',
                        increaseArea: '20%'
                    }) 

                    let dac_diem_vtri = ''
                    $.each(String(data.result).split("|"), function(i, r) {
                        dac_diem_vtri += `<div style="margin-left: 10px;">${r}</div>`
                    })
                    $("#dac_diem_vi_tri_thi_truong").html(dac_diem_vtri)
                            
                });
                return false;

            })

            
        
        // SET VALUE NONE 
        
            $("[id^='tinh_thanh_']").selectpicker("refresh").selectpicker("val","")
            $("[id^='vi_tri_']").selectpicker("refresh").selectpicker("val","")
            $("#du_an_cc_thi_truong").selectpicker("refresh").selectpicker("val","")
            $("#du_an_biet_thu").selectpicker("refresh").selectpicker("val","")
        
        
            // DELAY FUNC LIVESEARCH
            var delay = (function(){
            var timer = 0;
            return function(callback, ms){
                clearTimeout (timer);
                timer = setTimeout(callback, ms);
              };
            })();
            // LIVE SEARCH
            var list_keycode = [13,37,38,39,40,16,17,18,32]
            $(document).on("keyup",'div#div_dia_chi_thi_truong > div.bootstrap-select > div.dropdown-menu > div.bs-searchbox > input',function(e) {
                if(list_keycode.indexOf(e.keyCode) == -1 ){
                    let value = $(this).val().trim(); // remove any spaces around the text
                    delay(function(){                                            
                        if(value != ""){ // don't make requests with an empty string
                            $.ajax({
                                url: "/ajax_get_option_bds_nha_tho_cu_test",
                                data: {searchText: value},
                                dataType: "json",
                                type: "POST",
                                success: function(data){
                                    // create the html with results
                                    $("#dia_chi_thi_truong").empty()
                                    $.each(data.results,function(i,r) {
                                        $("#dia_chi_thi_truong").append(`<option>${r}</option>`)
                                    })
                                    $("#dia_chi_thi_truong").selectpicker('refresh')
                                    $("#dia_chi_thi_truong").selectpicker('val','')

                                    $("ul > li").removeClass("hidden")
                                    $("li.no-results").css("display","none")
                                }
                            })
                        // $(this).focus().attr("style","border-color:red !important")
                        // $("#dia_chi_thi_truong").selectpicker('val','')
                        }
                        else{
                            $("#dia_chi_thi_truong").selectpicker('refresh'); // set the results empty in case of empty string
                            $("ul > li").removeClass("hidden")
                            $("li.no-results").css("display","none")
                            $("#dia_chi_thi_truong").selectpicker('val','')
                        }
                    },300);
                }
                
            // $("#dia_chi_thi_truong").selectpicker('val','') 
            })    
        
        
            // $(document).on('click','#get_result', function() {
            //     let list_yeu_to = []
            //     $.each($.merge($(`input[id^='check_box_loi_the']`), $(`input[id^='check_box_bat_loi']`)), function(i,r) {
            //         if($(this).is(':checked') == true) {
            //             list_yeu_to.push($(this).val())
                        
            //         }
            //     })
            //     console.log(list_yeu_to.join("|"))

            // })
        
        // AXAX BDS THO CU 
        
            $(`#hinh_dang`).selectpicker("refresh").selectpicker("val","")
            // FUNCTION EMPTY FIELD
            function empty_field() {
                $("#dien_tich_dat_thi_truong").val("")
                $("#do_rong_mat_tien_thi_truong").val("")
                $("#do_rong_ngo_thi_truong").val("")
                $("#kcach_truc_chinh_thi_truong").val("")
                $(`#hinh_dang`).selectpicker("val","").selectpicker("refresh")              
                $("#dac_diem_vi_tri_thi_truong").text("")
                $("#gia_sau").text("")
            }

            // QUAN HUYEN AJAX
                $(document).on('change','[id^="tinh_thanh_"]', function() {

                    let tinh_thanh_id = $(this).attr("id")
                    let quan_huyen_id = `quan_huyen_${tinh_thanh_id.split("tinh_thanh_")[1]}`
                    let ten_duong_id = `ten_duong_${tinh_thanh_id.split("tinh_thanh_")[1]}`
                    let tuyen_duong_id = `tuyen_duong_${tinh_thanh_id.split("tinh_thanh_")[1]}`
                    let vi_tri_bds_id = `vi_tri_bds_${tinh_thanh_id.split("tinh_thanh_")[1]}`

                    // EMPTY FIELD ONCHANGE
                    empty_field()
                    // AJAX
                    $.getJSON($SCRIPT_ROOT + '/ajax_get_option_quan_huyen', {
                        tinh_thanh: $(this).val(),
                    }, function(data) { 
                        
                        // empty field                        
                        $(`#${quan_huyen_id}`).empty().prop("disabled",true)
                        $(`#${ten_duong_id}`).empty().prop("disabled",true)
                        $(`#${tuyen_duong_id}`).empty().prop("disabled",true)
                        $(`#${vi_tri_bds_id}`).empty().prop("disabled",true)
                        $(`[id^="gia_tri_tai_san_"]`).empty()
                        $("#div_select_loi_the").empty()
                        $("#div_select_bat_loi").empty()

                        $.each(data.result, function(i,r) {
                            $(`#${quan_huyen_id}`).append(`<option>${r}</option>`).prop("disabled",false)
                        })
                        $(`#${quan_huyen_id}`).selectpicker("refresh").selectpicker("val","")
                        $(`#${ten_duong_id}`).selectpicker("refresh").selectpicker("val","")
                        $(`#${tuyen_duong_id}`).selectpicker("refresh").selectpicker("val","")
                        $(`#${vi_tri_bds_id}`).selectpicker("refresh").selectpicker("val","")

                      })
                      return false;
                })
            // DOAN DUONG AJAX
                $(document).on('change','[id^="quan_huyen_"]', function() {
                    let quan_huyen_id = $(this).attr("id")
                    let tinh_thanh_id = `tinh_thanh_${quan_huyen_id.split("quan_huyen_")[1]}`
                    let ten_duong_id = `ten_duong_${quan_huyen_id.split("quan_huyen_")[1]}`
                    let tuyen_duong_id = `tuyen_duong_${quan_huyen_id.split("quan_huyen_")[1]}`
                    let vi_tri_bds_id = `vi_tri_bds_${quan_huyen_id.split("quan_huyen_")[1]}`
                    empty_field()
                    // AJAX
                    $.getJSON($SCRIPT_ROOT + '/ajax_get_option_duong_pho', {
                        tinh_thanh: $(`#${tinh_thanh_id}`).val(),
                        quan_huyen: $(this).val(),

                    }, function(data) { 
                        $(`#${ten_duong_id}`).empty().prop("disabled",true)
                        $(`#${tuyen_duong_id}`).empty().prop("disabled",true)
                        $(`#${vi_tri_bds_id}`).empty().prop("disabled",true)
                        $(`[id^="gia_tri_tai_san_"]`).empty()
                        $("#div_select_loi_the").empty()
                        $("#div_select_bat_loi").empty()
                        $.each(data.result, function(i,r) {
                            $(`#${ten_duong_id}`).append(`<option>${r}</option>`).prop("disabled",false)
                        })
                        $(`#${ten_duong_id}`).selectpicker("refresh").selectpicker("val","")
                        $(`#${tuyen_duong_id}`).selectpicker("refresh").selectpicker("val","")
                        $(`#${vi_tri_bds_id}`).selectpicker("refresh").selectpicker("val","")

                      });
                      return false;
                })
            // TUYEN DUONG AJAX
                $(document).on('change','[id^="ten_duong_"]', function() {
                    let ten_duong_id = $(this).attr("id")
                    let tinh_thanh_id = `tinh_thanh_${ten_duong_id.split("ten_duong_")[1]}`
                    let quan_huyen_id = `quan_huyen_${ten_duong_id.split("ten_duong_")[1]}`
                    let tuyen_duong_id = `tuyen_duong_${ten_duong_id.split("ten_duong_")[1]}`
                    let vi_tri_bds_id = `vi_tri_bds_${ten_duong_id.split("ten_duong_")[1]}`
                    empty_field()
                    // AJAX
                    $.getJSON($SCRIPT_ROOT + '/ajax_get_option_tuyen_duong', {
                        tinh_thanh: $(`#${tinh_thanh_id}`).val(),
                        quan_huyen: $(`#${quan_huyen_id}`).val(),              
                        ten_duong: $(this).val(),

                    }, function(data) { 
                        $(`#${tuyen_duong_id}`).empty().prop("disabled",true)
                        $(`#${vi_tri_bds_id}`).empty().prop("disabled",true)
                        $(`[id^="gia_tri_tai_san_"]`).empty()
                        $("#div_select_loi_the").empty()
                        $("#div_select_bat_loi").empty()
                        $.each(data.result, function(i,r) {
                            $(`#${tuyen_duong_id}`).append(`<option>${r}</option>`).prop("disabled",false)
                        })
                        $(`#${tuyen_duong_id}`).selectpicker("refresh").selectpicker("val","")
                        $(`#${vi_tri_bds_id}`).selectpicker("refresh").selectpicker("val","")

                      });
                      return false;
                })
            // VI TRI BDS AJAX
                $(document).on('change','[id^="tuyen_duong_"]', function() {
                    let tuyen_duong_id = $(this).attr("id")
                    let tinh_thanh_id = `tinh_thanh_${tuyen_duong_id.split("tuyen_duong_")[1]}`
                    let quan_huyen_id = `quan_huyen_${tuyen_duong_id.split("tuyen_duong_")[1]}`
                    let ten_duong_id = `ten_duong_${tuyen_duong_id.split("tuyen_duong_")[1]}`
                    let vi_tri_bds_id = `vi_tri_bds_${tuyen_duong_id.split("tuyen_duong_")[1]}`
                    empty_field()
                    // AJAX
                    $.getJSON($SCRIPT_ROOT + '/ajax_get_option_vi_tri_bds', {
                        tinh_thanh: $(`#${tinh_thanh_id}`).val(),
                        quan_huyen: $(`#${quan_huyen_id}`).val(),
                        ten_duong: $(`#${ten_duong_id}`).val(),            
                        tuyen_duong: $(this).val(),

                    }, function(data) { 

                        $(`#${vi_tri_bds_id}`).empty().prop("disabled",true)
                        $(`[id^="gia_tri_tai_san_"]`).empty()
                        $("#div_select_loi_the").empty()
                        $("#div_select_bat_loi").empty()
                        $.each(data.result, function(i,r) {
                            $(`#${vi_tri_bds_id}`).append(`<option>${r}</option>`).prop("disabled",false)
                        })
                        $(`#${vi_tri_bds_id}`).selectpicker("refresh").selectpicker("val","")
                      });
                      return false;
                })
            ////// DIA CHI CHANGE
                // $(document).on('change','#dia_chi_thi_truong', function() {

                //     $.getJSON($SCRIPT_ROOT + '/ajax_get_option_bds_nha_tho_cu', {
                //       dia_chi_thi_truong: $("#dia_chi_thi_truong").val(),
                //     }, function(data) { 
                //         $("#ten_duong_thi_truong").empty().prop("disabled",true)
                //         $.each(data.result, function(i,r) {
                //             $("#ten_duong_thi_truong").append(`<option>${r}</option>`).prop("disabled",false)
                //         })
                //         $("#ten_duong_thi_truong").selectpicker("refresh").selectpicker("val","")
                //       });
                //       return false;
                // })
        
        // AJAX BDS CAN HO 
        
            // GET TEN TOA NHA
            $(document).on('change','[id^="du_an_cc_thi_truong"]', function() {
                $.getJSON($SCRIPT_ROOT + '/ajax_get_option_du_an_can_ho', {            
                    ten_du_an: $(this).val(),
                }, function(data) { 
                    $(`#toa_nha_cc_thi_truong`).empty().prop("disabled",true)
                    $(`#tang_cc_thi_truong`).empty().prop("disabled",true)
                    $(`#ma_can_cc_thi_truong`).empty().prop("disabled",true)
                    $(`[id^="value_"]`).empty()               

                    $.each(data.result, function(i,r) {
                        $(`#toa_nha_cc_thi_truong`).append(`<option>${r}</option>`).prop("disabled",false)
                    })
                    $(`#toa_nha_cc_thi_truong`).selectpicker("refresh").selectpicker("val","")
                    $(`#tang_cc_thi_truong`).selectpicker("refresh").selectpicker("val","")
                    $(`#ma_can_cc_thi_truong`).selectpicker("refresh").selectpicker("val","")
                  });
                  return false;
            })
            // GET SO TANG NHA
                $(document).on('change','[id^="toa_nha_cc_thi_truong"]', function() {
                    $.getJSON($SCRIPT_ROOT + '/ajax_get_option_tang_can_ho', { 
                        ten_du_an: $("#du_an_cc_thi_truong").val(),
                        ten_toa_nha: $(this).val(),
                    }, function(data) { 
                        $(`#tang_cc_thi_truong`).empty().prop("disabled",true)
                        $(`#ma_can_cc_thi_truong`).empty().prop("disabled",true)
                        $(`[id^="value_"]`).empty()               

                        $.each(data.result, function(i,r) {
                            $(`#tang_cc_thi_truong`).append(`<option>${r}</option>`).prop("disabled",false)
                        })
                        $(`#tang_cc_thi_truong`).selectpicker("refresh").selectpicker("val","")
                        $(`#ma_can_cc_thi_truong`).selectpicker("refresh").selectpicker("val","")

                      });
                      return false;
                })
            // GET MA CAN
                $(document).on('change','[id^="tang_cc_thi_truong"]', function() {
                    $.getJSON($SCRIPT_ROOT + '/ajax_get_option_ma_can_ho', { 
                        ten_du_an: $("#du_an_cc_thi_truong").val(),
                        ten_toa_nha: $("#toa_nha_cc_thi_truong").val(),
                        so_tang: $(this).val(),

                    }, function(data) { 
                        $(`#ma_can_cc_thi_truong`).empty().prop("disabled",true)
                        $(`[id^="value_"]`).empty()               
                        $.each(data.result, function(i,r) {
                            $(`#ma_can_cc_thi_truong`).append(`<option>${r}</option>`).prop("disabled",false)
                        })
                        $(`#ma_can_cc_thi_truong`).selectpicker("refresh").selectpicker("val","")
                      });
                      return false;
                })
            // GET VALUE
                $(document).on('change','[id^="ma_can_cc_thi_truong"]', function() {
                    $.getJSON($SCRIPT_ROOT + '/ajax_get_option_gia_can_ho', { 
                        ten_du_an: $("#du_an_cc_thi_truong").val(),
                        ten_toa_nha: $("#toa_nha_cc_thi_truong").val(),
                        so_tang: $("#tang_cc_thi_truong").val(),
                        ma_can: $("#ma_can_cc_thi_truong").val(),
                    }, function(data) { 
                        $("#result_chung_cu").css("display", "")
                        $("#value_dien_tich_cc_thi_truong").text(data.result[0][0])
                        $("#value_loai_dien_tich_cc_thi_truong").text(data.result[0][1])
                        $("#value_don_gia_cc_thi_truong").text(dot_number(Math.round(data.result[0][2])))
                        $("#value_ghi_chu_cc_thi_truong").text(data.result[0][3])
                      });
                      return false;
                })
        
        // AJAX BDS BIET THU 

            // GET TEN DUONG
                $(document).on('change','[id^="du_an_biet_thu"]', function() {
                    $.getJSON($SCRIPT_ROOT + '/ajax_get_option_ten_duong_biet_thu', { 
                        ten_du_an: $("#du_an_biet_thu").val(),
                    }, function(data) { 
                        $(`#duong_nha_biet_thu`).empty().prop("disabled",true)
                        $(`#loai_nha_biet_thu`).empty().prop("disabled",true)
                        $(`#ma_can_biet_thu`).empty().prop("disabled",true)
                        $(`[id^="value_"]`).empty()          
                
                        $.each(data.result, function(i,r) {
                            $(`#duong_nha_biet_thu`).append(`<option>${r}</option>`).prop("disabled",false)
                        })
                        $(`#duong_nha_biet_thu`).selectpicker("refresh").selectpicker("val","")
                        $(`#loai_nha_biet_thu`).selectpicker("refresh").selectpicker("val","")
                        $(`#ma_can_biet_thu`).selectpicker("refresh").selectpicker("val","")
                      });
                      return false;
                })
                // GET LOAI NHA
                    $(document).on('change','[id^="duong_nha_biet_thu"]', function() {
                        $.getJSON($SCRIPT_ROOT + '/ajax_get_option_tang_biet_thu', { 
                            ten_du_an: $("#du_an_biet_thu").val(),
                            ten_duong: $("#duong_nha_biet_thu").val(),
                        }, function(data) { 
                            $(`#loai_nha_biet_thu`).empty().prop("disabled",true)
                            $(`#ma_can_biet_thu`).empty().prop("disabled",true)             
                            $(`[id^="value_"]`).empty() 
                            $.each(data.result, function(i,r) {
                                $(`#loai_nha_biet_thu`).append(`<option>${r}</option>`).prop("disabled",false)
                            })
                            $(`#loai_nha_biet_thu`).selectpicker("refresh").selectpicker("val","")
                            $(`#ma_can_biet_thu`).selectpicker("refresh").selectpicker("val","")

                          });
                          return false;
                    })
                    // GET MA CAN
                        $(document).on('change','[id^="loai_nha_biet_thu"]', function() {
                            $.getJSON($SCRIPT_ROOT + '/ajax_get_option_ma_biet_thu', { 
                                ten_du_an: $("#du_an_biet_thu").val(),
                                ten_duong: $("#duong_nha_biet_thu").val(),
                                ten_tang: $(this).val(),

                            }, function(data) { 
                                $(`#ma_can_biet_thu`).empty().prop("disabled",true)
                                $(`[id^="value_"]`).empty()             
                                $.each(data.result, function(i,r) {
                                    $(`#ma_can_biet_thu`).append(`<option>${r}</option>`).prop("disabled",false)
                                })
                                $(`#ma_can_biet_thu`).selectpicker("refresh").selectpicker("val","")
                              });
                              return false;
                        })
                    // GET VALUE
                        $(document).on('change','[id^="ma_can_biet_thu"]', function() {
                            $.getJSON($SCRIPT_ROOT + '/ajax_get_option_gia_biet_thu', { 
                                ten_du_an: $("#du_an_biet_thu").val(),
                                ten_duong: $("#duong_nha_biet_thu").val(),
                                ten_tang: $("#loai_nha_biet_thu").val(),
                                ma_can: $("#ma_can_biet_thu").val(),
                            }, function(data) { 
                                $("#result_biet_thu").css("display", "")
                                console.log(data.result)
                                $("#value_dien_tich_biet_thu").text(data.result[0][0])
                                $("#value_dien_tich_san_biet_thu").text(data.result[0][1])
                                $("#value_tong_gia_tho_biet_thu").text(data.result[0][2])
                                $("#value_tong_gia_full_biet_thu").text(data.result[0][3])
                                $("#value_don_gia_dat").text(dot_number(Math.round(data.result[0][4])))
                                $("#value_don_gia_ctxd").text(dot_number(Math.round(data.result[0][5])))
                              });
                              return false;
                        })
