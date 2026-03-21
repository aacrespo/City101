

function ouvre_vb (pExterne)
	{
		$("body").css("overflow", "hidden");
		const tFrame = $("#vb");
		if (!tFrame.length)
			{
				$.post( "/visuelbat/cree_ticket_vb.php", function (res)
					{											
						if (pExterne)
							{
								$("body").append ('<div id="vb_overlay" class="vb_non_selectionnable"><div id="vb_cadre"><iframe id="vb"></iframe></div></div>');								
							}
						else
							{
								$("body").append ('<div id="vb_overlay" class="vb_non_selectionnable"><div id="vb_cadre"><iframe id="vb"></iframe></div><div class= "vb_bouton vb_bouton_barre_outils vb_droite" id="vb_bouton_sortie" onclick="ferme_vb()" title="Fermer VisuelBAT"><img src="/visuelbat/img/bouton_x.svg" /></div></div>');								
							}
						const tIframe = $('#vb');
						tIframe.remove();
						tIframe.attr('src', res);
						tIframe.attr('onmousewheel', "");
						$("#vb_cadre").append (tIframe);													
						$("#vb_overlay")
							.css("z-index", 1000)
							.show()
							.animate ({ opacity: 1 }, 1000, function() {})
						;
/*
						var iframeEvent = new Event('wheel_externe');
						
						$("#vb_overlay")[0].addEventListener('wheel', function (e)
							{
							   	console.log (e);
							    $("#vb")[0].dispatchEvent(iframeEvent);
							});
						
						$("#vb")[0].addEventListener('wheel_externe', function (e)
							{
							    console.log(e);
							});	
*/						
							
					});
			}
		else
			{
				$("#vb_overlay")	
					.show()
					.animate ({ opacity: 1 }, 1000, function() {});							
			}			
	}
	
function ferme_vb ()
	{
		$("#vb_overlay").animate ({ opacity: 0, }, 500, function() { $("#vb_overlay").hide(); });
		$("body").css("overflow", "unset");
	}
	
function ferme_iframe_vb ()
	{
		$("#vb_overlay").animate ({ opacity: 0, }, 500, function() { $("#vb_overlay").remove(); });
		$("body").css("overflow", "unset");
	}
