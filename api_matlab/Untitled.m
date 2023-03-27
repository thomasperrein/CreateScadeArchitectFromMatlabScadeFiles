% a = fieldnames(get_param('F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP/From8','ObjectParameters'));
% for i=1:numel(a)
%     disp(a{i,1})
%     disp(get_param('F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP/From8',a{i,1}))
% end

disp('other')

b = fieldnames(get_param('F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP/BCM_COM_PROC_P20/V_BCM_COM_Tachometers_Conf_Flt','ObjectParameters'));
for i=1:numel(b)
    disp(b{i,1})
    disp(get_param('F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP/BCM_COM_PROC_P20/V_BCM_COM_Tachometers_Conf_Flt',b{i,1}))
end

c = get_param('F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP/BCM_COM_PROC_P20/V_BCM_COM_RH_Decel_Law_Brkg_Press_Cmd','Port')