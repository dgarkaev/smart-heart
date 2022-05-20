function [info, status]=pcg_info(fn)
try
    status=true;
    info=audioinfo(fn);
catch err
    info=err.message;
    status=false;
end
end