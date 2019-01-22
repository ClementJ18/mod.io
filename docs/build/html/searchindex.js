Search.setIndex({docnames:["client","enums","errors","filtering&sorting","game","index","mod","objects","utils"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.intersphinx":1,"sphinx.ext.viewcode":1,sphinx:55},filenames:["client.rst","enums.rst","errors.rst","filtering&sorting.rst","game.rst","index.rst","mod.rst","objects.rst","utils.rst"],objects:{"modio.client":{Client:[0,1,1,""]},"modio.client.Client":{BASE_PATH:[0,2,1,""],account_link:[0,3,1,""],email_exchange:[0,3,1,""],email_request:[0,3,1,""],get_game:[0,3,1,""],get_games:[0,3,1,""],get_my_events:[0,3,1,""],get_my_games:[0,3,1,""],get_my_modfiles:[0,3,1,""],get_my_mods:[0,3,1,""],get_my_ratings:[0,3,1,""],get_my_subs:[0,3,1,""],get_my_user:[0,3,1,""],get_user:[0,3,1,""],get_users:[0,3,1,""],rate_limit:[0,2,1,""],rate_remain:[0,2,1,""],rate_retry:[0,2,1,""],steam_auth:[0,3,1,""]},"modio.enums":{APIAccess:[1,1,1,""],Community:[1,1,1,""],Curation:[1,1,1,""],EventType:[1,1,1,""],Level:[1,1,1,""],Maturity:[1,1,1,""],MaturityOptions:[1,1,1,""],Presentation:[1,1,1,""],RatingType:[1,1,1,""],Report:[1,1,1,""],Revenue:[1,1,1,""],Status:[1,1,1,""],Submission:[1,1,1,""],VirusStatus:[1,1,1,""],Visibility:[1,1,1,""]},"modio.enums.APIAccess":{direct_downloads:[1,2,1,""],disabled:[1,2,1,""],third_party:[1,2,1,""]},"modio.enums.Community":{disabled:[1,2,1,""],discussion_boards:[1,2,1,""],guides_news:[1,2,1,""]},"modio.enums.Curation":{full_curation:[1,2,1,""],no_curation:[1,2,1,""],paid_curation:[1,2,1,""]},"modio.enums.EventType":{available:[1,2,1,""],deleted:[1,2,1,""],edited:[1,2,1,""],file_changed:[1,2,1,""],other:[1,2,1,""],subscribe:[1,2,1,""],team_changed:[1,2,1,""],team_join:[1,2,1,""],team_leave:[1,2,1,""],unavailable:[1,2,1,""],unsubscribe:[1,2,1,""]},"modio.enums.Level":{admin:[1,2,1,""],creator:[1,2,1,""],moderator:[1,2,1,""]},"modio.enums.Maturity":{alcohol:[1,2,1,""],drugs:[1,2,1,""],explicit:[1,2,1,""],none:[1,2,1,""],violence:[1,2,1,""]},"modio.enums.MaturityOptions":{allowed:[1,2,1,""],forbidden:[1,2,1,""]},"modio.enums.Presentation":{grid:[1,2,1,""],table:[1,2,1,""]},"modio.enums.RatingType":{bad:[1,2,1,""],good:[1,2,1,""],neutral:[1,2,1,""]},"modio.enums.Report":{dmca:[1,2,1,""],generic:[1,2,1,""]},"modio.enums.Revenue":{disabled:[1,2,1,""],donations:[1,2,1,""],full_control:[1,2,1,""],sold:[1,2,1,""],traded:[1,2,1,""]},"modio.enums.Status":{accepted:[1,2,1,""],archived:[1,2,1,""],deleted:[1,2,1,""],not_accepted:[1,2,1,""]},"modio.enums.Submission":{restricted:[1,2,1,""],unrestricted:[1,2,1,""]},"modio.enums.VirusStatus":{error:[1,2,1,""],in_progress:[1,2,1,""],not_found:[1,2,1,""],not_scanned:[1,2,1,""],scan_complete:[1,2,1,""],too_large:[1,2,1,""]},"modio.enums.Visibility":{"public":[1,2,1,""],hidden:[1,2,1,""]},"modio.errors":{BadRequest:[2,4,1,""],Forbidden:[2,4,1,""],Gone:[2,4,1,""],MethodNotAllowed:[2,4,1,""],NotAcceptable:[2,4,1,""],NotFound:[2,4,1,""],TooManyRequests:[2,4,1,""],Unauthorized:[2,4,1,""],UnprocessableEntity:[2,4,1,""],modioException:[2,4,1,""]},"modio.errors.BadRequest":{args:[2,2,1,""],with_traceback:[2,3,1,""]},"modio.errors.Forbidden":{args:[2,2,1,""],with_traceback:[2,3,1,""]},"modio.errors.Gone":{args:[2,2,1,""],with_traceback:[2,3,1,""]},"modio.errors.MethodNotAllowed":{args:[2,2,1,""],with_traceback:[2,3,1,""]},"modio.errors.NotAcceptable":{args:[2,2,1,""],with_traceback:[2,3,1,""]},"modio.errors.NotFound":{args:[2,2,1,""],with_traceback:[2,3,1,""]},"modio.errors.TooManyRequests":{args:[2,2,1,""],with_traceback:[2,3,1,""]},"modio.errors.Unauthorized":{args:[2,2,1,""],with_traceback:[2,3,1,""]},"modio.errors.UnprocessableEntity":{args:[2,2,1,""],errors:[2,2,1,""],with_traceback:[2,3,1,""]},"modio.errors.modioException":{args:[2,2,1,""],with_traceback:[2,3,1,""]},"modio.game":{Game:[4,1,1,""]},"modio.game.Game":{add_media:[4,3,1,""],add_mod:[4,3,1,""],add_tag_options:[4,3,1,""],api:[4,2,1,""],community:[4,2,1,""],curation:[4,2,1,""],date:[4,2,1,""],delete_tag_options:[4,3,1,""],edit:[4,3,1,""],get_mod:[4,3,1,""],get_mod_events:[4,3,1,""],get_mods:[4,3,1,""],get_owner:[4,3,1,""],get_stats:[4,3,1,""],get_tag_options:[4,3,1,""],header:[4,2,1,""],icon:[4,2,1,""],id:[4,2,1,""],instructions:[4,2,1,""],instructions_url:[4,2,1,""],live:[4,2,1,""],logo:[4,2,1,""],maturity_options:[4,2,1,""],name:[4,2,1,""],name_id:[4,2,1,""],presentation:[4,2,1,""],profile:[4,2,1,""],report:[4,3,1,""],revenue:[4,2,1,""],status:[4,2,1,""],submission:[4,2,1,""],submitter:[4,2,1,""],summary:[4,2,1,""],tag_options:[4,2,1,""],ugc:[4,2,1,""],updated:[4,2,1,""]},"modio.mod":{Mod:[6,1,1,""]},"modio.mod.Mod":{"delete":[6,3,1,""],add_dependencies:[6,3,1,""],add_file:[6,3,1,""],add_media:[6,3,1,""],add_metadata:[6,3,1,""],add_negative_rating:[6,3,1,""],add_positive_rating:[6,3,1,""],add_tags:[6,3,1,""],add_team_member:[6,3,1,""],date:[6,2,1,""],delete_dependencies:[6,3,1,""],delete_media:[6,3,1,""],delete_metadata:[6,3,1,""],delete_tags:[6,3,1,""],description:[6,2,1,""],edit:[6,3,1,""],file:[6,2,1,""],game:[6,2,1,""],get_comments:[6,3,1,""],get_dependencies:[6,3,1,""],get_events:[6,3,1,""],get_file:[6,3,1,""],get_files:[6,3,1,""],get_metadata:[6,3,1,""],get_owner:[6,3,1,""],get_stats:[6,3,1,""],get_tags:[6,3,1,""],get_team:[6,3,1,""],homepage:[6,2,1,""],id:[6,2,1,""],kvp:[6,2,1,""],live:[6,2,1,""],logo:[6,2,1,""],maturity:[6,2,1,""],media:[6,2,1,""],metadata:[6,2,1,""],name:[6,2,1,""],name_id:[6,2,1,""],plaintext:[6,2,1,""],profile:[6,2,1,""],rating:[6,2,1,""],report:[6,3,1,""],status:[6,2,1,""],submitter:[6,2,1,""],subscribe:[6,3,1,""],summary:[6,2,1,""],tags:[6,2,1,""],unsubscribe:[6,3,1,""],updated:[6,2,1,""],visible:[6,2,1,""]},"modio.objects":{Comment:[7,1,1,""],Dependencies:[7,1,1,""],Event:[7,1,1,""],Filter:[7,1,1,""],Image:[7,1,1,""],Message:[7,1,1,""],MetaData:[7,1,1,""],ModFile:[7,1,1,""],ModMedia:[7,1,1,""],NewMod:[7,1,1,""],NewModFile:[7,1,1,""],Object:[7,1,1,""],Pagination:[7,1,1,""],Rating:[7,1,1,""],Returned:[7,1,1,""],Stats:[7,1,1,""],Tag:[7,1,1,""],TagOption:[7,1,1,""],TeamMember:[7,1,1,""],User:[7,1,1,""]},"modio.objects.Comment":{"delete":[7,3,1,""],children:[7,2,1,""],content:[7,2,1,""],date:[7,2,1,""],id:[7,2,1,""],karma:[7,2,1,""],karma_guest:[7,2,1,""],level:[7,2,1,""],mod:[7,2,1,""],parent:[7,2,1,""],position:[7,2,1,""],user:[7,2,1,""]},"modio.objects.Event":{date:[7,2,1,""],id:[7,2,1,""],mod:[7,2,1,""],type:[7,2,1,""],user:[7,2,1,""]},"modio.objects.Filter":{bitwise:[7,3,1,""],equals:[7,3,1,""],greater_than:[7,3,1,""],like:[7,3,1,""],limit:[7,3,1,""],max:[7,3,1,""],min:[7,3,1,""],not_equals:[7,3,1,""],not_like:[7,3,1,""],offset:[7,3,1,""],smaller_than:[7,3,1,""],sort:[7,3,1,""],text:[7,3,1,""],values_in:[7,3,1,""],values_not_in:[7,3,1,""]},"modio.objects.Image":{filename:[7,2,1,""],large:[7,2,1,""],medium:[7,2,1,""],original:[7,2,1,""],small:[7,2,1,""]},"modio.objects.Message":{code:[7,2,1,""],message:[7,2,1,""]},"modio.objects.ModFile":{"delete":[7,3,1,""],changelog:[7,2,1,""],date:[7,2,1,""],edit:[7,3,1,""],expire:[7,2,1,""],filename:[7,2,1,""],game:[7,2,1,""],get_owner:[7,3,1,""],hash:[7,2,1,""],id:[7,2,1,""],metadata:[7,2,1,""],mod:[7,2,1,""],scanned:[7,2,1,""],size:[7,2,1,""],url:[7,2,1,""],url_is_expired:[7,3,1,""],version:[7,2,1,""],virus:[7,2,1,""],virus_hash:[7,2,1,""],virus_status:[7,2,1,""]},"modio.objects.ModMedia":{images:[7,2,1,""],sketchfab:[7,2,1,""],youtube:[7,2,1,""]},"modio.objects.NewMod":{add_tags:[7,3,1,""]},"modio.objects.NewModFile":{add_file:[7,3,1,""]},"modio.objects.Pagination":{count:[7,2,1,""],limit:[7,2,1,""],max:[7,3,1,""],min:[7,3,1,""],next:[7,3,1,""],offset:[7,2,1,""],page:[7,3,1,""],previous:[7,3,1,""],total:[7,2,1,""]},"modio.objects.Rating":{"delete":[7,3,1,""],add_negative_rating:[7,3,1,""],add_positive_rating:[7,3,1,""],date:[7,2,1,""],game:[7,2,1,""],mod:[7,2,1,""],rating:[7,2,1,""]},"modio.objects.Returned":{count:[7,3,1,""],index:[7,3,1,""],pagination:[7,2,1,""],results:[7,2,1,""]},"modio.objects.Stats":{downloads:[7,2,1,""],expires:[7,2,1,""],id:[7,2,1,""],is_stale:[7,3,1,""],negative:[7,2,1,""],percentage:[7,2,1,""],positive:[7,2,1,""],rank:[7,2,1,""],rank_total:[7,2,1,""],subscribers:[7,2,1,""],text:[7,2,1,""],total:[7,2,1,""],weighted:[7,2,1,""]},"modio.objects.TagOption":{hidden:[7,2,1,""],name:[7,2,1,""],tags:[7,2,1,""],type:[7,2,1,""]},"modio.objects.TeamMember":{"delete":[7,3,1,""],avatar:[7,2,1,""],date:[7,2,1,""],edit:[7,3,1,""],id:[7,2,1,""],lang:[7,2,1,""],last_online:[7,2,1,""],level:[7,2,1,""],mod:[7,2,1,""],name_id:[7,2,1,""],position:[7,2,1,""],profile:[7,2,1,""],report:[7,3,1,""],team_id:[7,2,1,""],tz:[7,2,1,""],username:[7,2,1,""]},"modio.objects.User":{avatar:[7,2,1,""],id:[7,2,1,""],lang:[7,2,1,""],last_online:[7,2,1,""],name_id:[7,2,1,""],profile:[7,2,1,""],report:[7,3,1,""],tz:[7,2,1,""],username:[7,2,1,""]},"modio.utils":{concat_docs:[8,5,1,""],find:[8,5,1,""],get:[8,5,1,""]},modio:{client:[0,0,0,"-"],enums:[1,0,0,"-"],errors:[2,0,0,"-"],game:[4,0,0,"-"],mod:[6,0,0,"-"],objects:[7,0,0,"-"],utils:[8,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","method","Python method"],"4":["py","exception","Python exception"],"5":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:method","4":"py:exception","5":"py:function"},terms:{"10gb":7,"1280x720":[4,6],"128x128":4,"1mb":4,"256kb":4,"256x256":4,"320x180":[4,6],"3rd":[1,4],"400x100":4,"640x360":[4,6],"64x64":4,"8mb":6,"byte":7,"case":[6,7],"class":[0,1,4,6,7,8],"default":[0,1,4,7],"enum":1,"function":[0,4,5,6,7],"import":[3,5],"int":[0,4,6,7],"long":0,"new":[1,4,6],"public":1,"return":[0,2,3,4,6,7,8],"true":[3,4,6,7],"try":[6,7],"var":6,"while":0,For:[3,4,6,7,8],NOT:[3,7],Not:[1,4],One:4,The:[0,1,2,3,4,6,7],There:7,These:[1,6,7],Use:7,Used:[4,6,7],Will:6,__traceback__:2,about:6,abov:[1,3,7],accept:1,access:[0,1,2,4,6,7],access_token:0,accomplish:7,account_link:0,action:2,activ:7,add:[3,4,5,6,7],add_depend:6,add_fil:[6,7],add_media:[4,6],add_metadata:6,add_mod:[4,7],add_negative_r:[6,7],add_positive_r:[6,7],add_tag:[6,7],add_tag_opt:4,add_team_memb:6,added:[0,1,4,6,7],addit:[3,7],addon:4,address:0,admin:[1,6,7],adress:5,advanc:7,after:[6,7],again:[0,7],against:7,ago:0,aka:0,alcohol:1,alia:7,all:[0,1,3,4,6,7,8],allow:[0,1,4,6,7],along:7,alphanumer:6,alreadi:[4,6,7],also:[0,3,6,7],amount:7,ani:[3,7],anywher:1,api:[0,1,2,3,4,5,6],api_kei:[0,3,5],apiaccess:[1,4],appear:7,appli:[4,7],applic:4,appropi:[4,6,7],appropri:7,archiv:1,arg:2,argmument:0,argument:[0,4,6,7],arrai:[4,7],ascend:[3,7],asset:3,attach:[3,6,7],attempt:7,attr:[4,6,7,8],attribut:[0,4,6,7],attributeerror:[6,7],auth:[0,5],authent:[0,5,6,7],authentifi:0,authentit:0,author:[6,7],avail:[0,1,2,4,7],availa:0,avala:7,avatar:7,background:4,bad:[1,6],badrequest:2,base:[0,1,2,4,6,7],base_path:0,basic:[],becom:[0,7],been:[0,4,6,7],befor:7,being:[6,7],belong:7,below:[1,5,7],best:7,between:4,binari:7,bit:7,bitwis:7,blank:4,board:1,bool:[0,4,7],bot:0,both:[3,5,7],brief:7,calcul:7,call:[3,6,7],can:[0,1,3,4,5,6,7],cannot:[0,2,4,6,7],categori:7,caus:[6,7],certain:7,chain:7,chanc:7,chang:[0,1,4,7],changelog:7,charact:[4,6,7],charg:6,check:[5,7],checkbox:[4,7],children:[6,7],choos:[1,7],chose:[4,7],chosen:7,citi:7,clementj18:5,client:[3,5,8],close:5,cls:8,code:[0,5,7],coincident:7,collect:[0,7],color:4,column:[3,7],columnnam:7,com:5,combin:7,comment1:[],comment2:[],comment3:[],comment4:[],comment5:[],comment:[6,7],commun:[1,4],compar:1,compat:7,complet:1,complex:0,compliant:0,compos:7,concat_doc:8,condit:7,confid:7,confirm:[0,6],connect:7,consid:7,construct:6,contain:[1,3,4,6,7],content:[1,2,4,5,7],context:7,control:1,convert:6,correspond:6,could:2,count:7,countri:7,creat:[0,1,4,6],creator:[1,4],criteria:3,curat:[1,4],current:7,custom:[1,7],d500d733c07c20e40a49fa32452b905dcc85b160:5,dark:4,dash:6,data:[3,6,7],date:[4,6,7],date_ad:[6,7],datetim:[4,6,7],decid:1,deepest:7,delet:[0,1,4,6,7],delete_depend:6,delete_media:6,delete_metadata:6,delete_tag:6,delete_tag_opt:4,deped:7,depend:[4,6,7],dependeci:6,dependency_id:6,depth:3,descend:[3,7],describ:[4,7],descript:[4,6,7],desir:4,detail:[0,4,6,7],detect:7,dev:[1,4],develop:[1,6,7],developp:1,dict:[2,6,7],dictionnari:[6,7],difficulti:6,digit:0,dimens:[4,6],direct_download:1,directli:[0,1,7],directori:7,disabl:[1,4,6,7],discuss:1,discussion_board:1,displai:[1,4,6],dmca:1,doc:[3,7],document:0,doe:[7,8],don:[1,5,7],donat:1,download:[1,6,7],dropdown:[4,7],drug:1,dud:7,due:2,duplic:[6,7],each:7,easi:[1,5,6],easier:7,easili:3,edit:[0,1,3,4,5,6,7],either:[0,5,6,7],els:7,email:[0,5,6],email_exchang:[0,5],email_request:[0,5],empti:[6,8],enabl:[1,7],encourag:6,endpoint:[1,6,7],english:0,enjoi:8,enter:0,entir:4,entri:[7,8],enumer:5,environ:0,equal:[3,4,7,8],equival:7,error:[1,5,7],escap:[6,7],etc:[4,6],event:[0,1,4,6,7],eventtyp:[1,7],everi:[3,6,7],exactli:7,exampl:[3,6,7,8],exce:[4,6,7],except:5,exchang:0,exist:[4,7],expir:7,explain:[3,4],explicit:1,extend:3,fail:7,fals:[0,4,6,7],faq:6,featur:6,fewer:7,field:[4,6,7,8],file:[1,4,5,6,7],file_chang:1,filenam:[6,7],files:[4,6,7],filter:[0,4,5,6,7],find:8,fine:[3,7],fire:[0,6,7],first:[3,4,6,7,8],five:3,flag:1,flatten:6,fluid:7,folder:7,follow:[2,3,4,5,6,7],forbidden:[0,1,2,7],forget:5,form:[2,3],format:[4,6,7],found:[0,1,2,4,6,8],frame:2,frequent:1,from:[0,1,4,6,7],full:[1,7],full_control:1,full_cur:1,galleri:[6,7],game:[0,1,3,5,6,7,8],game_id:0,game_nam:6,gather:3,gener:[0,1,4,6,7],get:[0,3,4,6,8],get_all_gam:8,get_com:6,get_depend:6,get_ev:6,get_fil:6,get_gam:[0,3,5,7],get_metadata:6,get_mod:[4,5],get_mod_ev:4,get_my_ev:0,get_my_gam:0,get_my_mod:0,get_my_modfil:0,get_my_r:[0,7],get_my_sub:0,get_my_us:0,get_own:[4,6,7],get_stat:[4,6],get_tag:6,get_tag_opt:4,get_team:6,get_us:0,gif:[4,6],git:5,github:5,given:[0,4,7],goe:3,gone:2,good:[1,6,7],grant:[6,7],greater:7,greater_than:7,grid:1,gropup:7,group:[4,7],guest:7,guid:[1,4],guides_new:1,handl:1,hard:6,has:[0,4,6,7,8],hash:[1,7],have:[0,2,4,5,7,8],header:[2,4,7],help:[3,4,6,7],here:[3,5,7],hidden:[1,4,7],high:[4,6,7],higher:7,hit:0,homepag:[6,7],how:[4,6,7],html:[6,7],http:[4,6,7],icon:[4,7],identifi:7,ids:6,ignord:7,imag:[4,6,7],immedi:1,in_progress:1,includ:[0,1,4,6,7],incorrect:2,index:[5,7],inform:[4,6,7],inherit:7,initializi:0,input:5,insensit:6,inspect:2,instal:6,instanc:[0,3,4,6,7],instanti:[3,7],instead:7,instruct:[4,6],instructions_url:4,integ:7,intern:7,interv:7,intflag:1,invalid:[0,2],investig:[4,6,7],is_stal:7,isnt:[4,6,7],iso:0,istanc:7,item:[4,6,7,8],iter:8,its:[0,6],itself:[6,7],john:8,jpg:[4,6],just:6,karma:7,karma_guest:7,keep:7,kei:[0,2,3,5,6,7],keyword:[0,6,7],know:7,kvp:6,kwarg:7,label:7,lack:7,lang:[0,7],languag:[0,7],larg:[1,7],last:[3,4,6,7],last_onlin:7,latest:[0,4,6,7],learn:4,least:[4,6],left:4,lengh:6,lenient:7,less:0,level:[0,1,4,6,7],lib:[2,7],librari:[0,3,5,7],light:4,like:[3,7,8],limit:[0,3,6,7],link:[4,6,7],list:[1,4,6,7,8],live:[4,6,7],local:[0,7],logo:[4,6,7],longer:2,look:8,lord:[3,7],made:[0,2,7],mai:[6,7],make:[0,4,5,6,7],malform:2,manag:7,mani:[2,7],manual:4,mark:7,match:7,matur:[1,4,6,7],maturity_opt:4,maturityopt:[1,4],max:7,maximium:[6,7],maximum:7,md5:7,measur:7,media:[4,6,7],medium:[6,7],meet:[3,7],member:[0,7],menu:4,messag:[2,4,6,7],met:4,meta:6,metad:6,metadata:[3,6,7],metadata_blob:7,metakei:[6,7],metavalu:[6,7],method:[2,3,7],methodnotallow:2,min:7,minut:0,misc:5,miss:0,mod:[0,1,4,5],mod_team_chang:[6,7],modder:4,model:[0,5],moder:[1,4,6,7],modfil:[0,6,7],modifi:6,modio:[0,1,2,3,4,6,7,8],modioexcept:[2,4,6],modmedia:[6,7],modul:5,mordor:5,more:[0,4,7],most:[0,6],msg:2,multipl:[4,6,7],must:[1,4,6,7],name:[0,3,4,5,6,7,8],name_id:[4,6,7],necro:5,need:[0,5,6,7],neg:[6,7],nest:7,neutral:[1,7],newli:4,newmod:[4,7],newmodfil:[6,7],next:[3,7],next_pag:3,no_cur:1,none:[0,1,4,6,7,8],not_accept:1,not_equ:7,not_found:1,not_lik:[3,7],not_scan:1,notaccept:2,notfound:[0,2,4,6],now:5,number:[0,6,7],oauth2:[0,5],oauth:[],object:[0,3,4,6,7],obtain:[3,5,7],occur:1,occurr:7,offici:[6,7],offset:[3,7],onc:[0,5,7],one:[4,7],onli:[4,6,7],onlin:7,open:5,option:[0,1,4,6,7],order:[3,5,7],origin:[4,6,7],other:[1,6,7],over:7,overal:7,overview:7,overwrit:7,overwritten:4,own:5,pack:3,packag:5,page:[3,4,5,6,7],pagin:[0,4,5,6,7],pagination_metadata:3,paid:1,paid_cur:1,pair:6,param:6,paramat:3,paramet:[0,2,3,4,6,7],parent:7,part:[4,7],parti:[1,4],particular:0,pass:[3,6,7],path:[4,6,7],per:7,percentag:7,perform:[2,5],permiss:[2,6,7],pick:[0,4,7],pip:5,pistol_dmg:6,place:7,plai:1,plaintext:6,png:[4,6],poll:7,popular:6,posit:[6,7],positev:7,possibl:7,post:[0,7],pre:7,preced:7,prefer:7,present:[1,4,7],previou:7,previous:7,primari:7,print:5,proceed:3,process:[2,6,7],profil:[4,6,7],progress:1,properti:[6,7],proprietari:7,provid:[0,3,4,5,6,7],python:5,queri:[0,4,6,7],rais:[0,4,6,7],rank:7,rank_tot:7,rate:[0,1,6,7],rate_limit:0,rate_remain:0,rate_retri:0,ratingtyp:[1,7],ratio:[4,6],reach:[3,7],read:[4,6,7],receiv:[0,1,7],recommend:[4,6],refer:0,regist:[4,6],regular:7,reject:0,releas:[6,7],relev:[4,6,7],remain:0,remov:[4,6,7],render:1,repl:5,replac:7,repli:[6,7],report:[1,4,6,7],repres:[0,4,6,7],represent:7,request:[0,2,4,5,6,7],requir:[4,6,7],res:7,reset:[0,2],resolut:[4,6],resourc:[2,4,6,7],respond:[4,6,7],respons:[0,7],rest:0,restrict:1,result:[0,3,4,6,7],retri:2,retriev:6,reus:7,revenu:[1,4],revers:[3,7],right:[],ring:[3,7],rogu:7,row:7,rubric:7,run:[5,6],same:7,save:[5,7],scan:[1,7],scan_complet:1,scarciti:1,score:7,script:5,search:[5,7],second:[0,7],section:3,secur:[0,5],see:7,select:4,self:[2,7],semant:2,sent:[0,5],seri:6,server:[2,7],servic:0,set:[1,2,4,6,7],should:[4,6,7],shouldn:0,shown:4,simpl:7,simpli:[0,3,5,7],simpliest:7,singl:7,site:4,size:7,sketchfab:[6,7],skip:[3,7],sleep:0,small:7,smaller:7,smaller_than:7,sold:1,some:7,someon:[1,7],sort:[0,4,5,6,7],sort_download:6,sort_popular:6,sort_rat:6,sort_subscrib:6,sourc:[0,1,2,4,6,7,8],span:7,specif:0,specifi:[0,7],spot:7,sql:7,stale:7,stand:7,start:7,stat:[4,6,7],statist:7,statu:[1,4,6,7],steam_auth:0,still:7,stock:[6,7],stop:[1,7],store:[5,6,7],str:[0,4,6,7],string:7,sub_domain:[4,6],subdomain:[4,6,7],submiss:[1,4,6],submit:[0,1,4,6,7],submitt:[4,6,7],subscrib:[0,1,6,7],succeed:3,success:[4,6,7],sucess:[4,6],sucessfulli:4,summari:[4,6,7],suppli:[0,1,2,4,6,7],support:[0,3,4,6,7],sure:[4,6,7],syntax:2,tabl:1,tag:[4,6,7],tag_opt:[4,6],tagopt:[4,7],take:[0,4,6,7],team:[0,6,7],team_chang:1,team_id:7,team_join:1,team_leav:1,teammemb:[6,7],test1:6,test2:6,test3:6,test:[0,6],text:[3,7],textual:7,textur:7,than:[0,7],thei:[1,2,6,7],them:[6,7,8],therefor:7,thi:[0,1,3,4,5,6,7,8],third_parti:1,those:7,three:[3,4,6,7],through:[0,7],thumbnail:[4,6],time:[2,7],timestamp:[4,6,7],timezon:7,titl:[6,7],togeth:[1,7],token:[0,2],too:[1,2],too_larg:1,tool:1,toomanyrequest:[0,2],top:[6,7],total:[6,7],tou:[4,6,7],trade:1,transform:7,transpar:4,tune:[3,7],tupl:[0,4,6,7],two:5,txt:5,type:[0,1,2,4,6,7],ugc:4,ugc_nam:4,unabl:2,unauthor:[0,1,2],unavail:1,under:3,understand:[4,6,7],union:6,uniqu:7,unix:[4,6,7],unless:[1,7],unprocessableent:2,unrestrict:1,unsubscrib:[1,6],until:[0,7],upack:6,updat:[4,6,7],upload:[0,1,4,6,7],upon:0,url:[1,4,6,7],url_is_expir:7,use:[0,1,4,5,6,7],used:[0,3,4,6,7],useful:7,user:[0,4,5,6,7],user_id:7,usernam:7,using:[0,6,7],usual:0,util:[5,6],valid:[0,6,7],valu:[3,4,6,7,8],valueerror:[0,4,7],values_in:[3,7],values_not_in:7,vari:7,variabl:5,variou:[3,7],verif:1,version:[0,7],via:[1,5],view:7,violenc:1,viru:7,virus_hash:7,virus_statu:7,virusstatu:[1,7],virustot:7,visibl:[1,6,7],want:[3,6],wasn:[4,7],websit:[0,1],weigh:6,weight:7,well:2,went:[4,6],were:4,what:[3,4,6,7],whe:7,when:7,where:[0,3,4,7],whether:[0,1,4,7],which:[0,3,4,5,6,7],who:0,whose:8,wih:6,wiki:4,wildcard:7,wilson:7,window:[6,7],wish:[1,4,6],witcher:3,with_traceback:2,within:7,without:3,word:[3,4,7],work:[4,5,6,7],would:8,wrapper:5,write:5,you:[0,2,3,4,5,6,7],your:[0,2,4,5,6,7],youtub:[6,7],zip:[6,7]},titles:["Client","Enumerators","Errors and Exceptions","Filtering, Sorting and Pagination","Games","Welcome to modio\u2019s documentation!","Mod","Misc mod.io Models","Utility Functions"],titleterms:{"function":8,access:5,basic:5,client:0,document:5,enumer:1,error:2,exampl:5,except:2,filter:3,game:4,get:5,indic:5,instal:5,misc:7,mod:[6,7],model:7,modio:5,oauth:5,pagin:3,sort:3,tabl:5,token:5,usag:5,util:8,welcom:5}})