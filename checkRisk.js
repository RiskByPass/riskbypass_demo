function checkRisk() {
    let riskbypass = {};
    riskbypass.akamai = checkAkamai();
    riskbypass.cloudflare = checkCloudflare();
    riskbypass.recaptcha = checkRecaptcha();
    riskbypass.datadome = checkDatadome();
    riskbypass.hcaptcha = checkHcaptcha();
    riskbypass.funcaptcha = checkFuncaptcha();
    riskbypass.kasada = checkKasada();
    riskbypass.awswaf = checkAwsWaf();
    riskbypass.incapsula = checkIncapsula();
    riskbypass.shapef5 = checkShapeF5();
    riskbypass.perimeterx = checkPerimeterX();
    true_risk = []
    for (let key in riskbypass) {
        if (riskbypass[key]) {
            true_risk.push(key)
        }
    }
    if(true_risk.length > 0){
        en_text = 'Find ' + true_risk.join(', ') + ' in the website, you can use https://riskbypass.com/ to solve it.'
        cn_text = '发现' + true_risk.join(', ') + ' 在网站中，你可以使用 https://riskbypass.com/ 来解决它。'
    } else {
        en_text = 'No any risk found'
        cn_text = '没有发现任何风控产品'
    }
    result = `    akamai:${riskbypass.akamai ? 'Yes' : 'No'}
    cloudflare:${riskbypass.cloudflare ? 'Yes' : 'No'}
    recaptcha:${riskbypass.recaptcha ? 'Yes' : 'No'}
    datadome:${riskbypass.datadome ? 'Yes' : 'No'}
    hcaptcha:${riskbypass.hcaptcha ? 'Yes' : 'No'}
    funcaptcha:${riskbypass.funcaptcha ? 'Yes' : 'No'}
    kasada:${riskbypass.kasada ? 'Yes' : 'No'}
    awswaf:${riskbypass.awswaf ? 'Yes' : 'No'}
    incapsula:${riskbypass.incapsula ? 'Yes' : 'No'}
    shapef5:${riskbypass.shapef5 ? 'Yes' : 'No'}
    perimeterx:${riskbypass.perimeterx ? 'Yes' : 'No'}
    `
    riskbypass.solver = 'https://riskbypass.com/'
    console.log(result);
    console.log('%c' + en_text, 'color: red; font-weight: bold; font-size: 32px;');
    console.log('%c' + cn_text, 'color: red; font-weight: bold; font-size: 32px;');
    return riskbypass;
}
function checkAkamai() {
    return window.bmak ? true : false;
}
function checkCloudflare() {
    return window.__cfBeacon ? true : false;
}
function checkRecaptcha() {
    return window.grecaptcha ? true : false;
}
function checkDatadome() {
    return (window.ddjskey || document.cookie.includes('datadome')) ? true : false;
}
function checkHcaptcha() {
    return window.hcaptcha ? true : false;
}
function checkFuncaptcha() {
    const hasScript = [...document.scripts].some(script =>
        script.src && script.src.includes('arkoselabs.com')
    );
    // 检查 link 标签
    const hasLink = [...document.querySelectorAll('link')].some(link =>
        link.href && link.href.includes('arkoselabs.com')
    );
    // 检查 iframe 标签
    const hasIframe = [...document.querySelectorAll('iframe')].some(iframe =>
        iframe.src && iframe.src.includes('arkoselabs.com')
    );
    return hasScript || hasLink || hasIframe;
}
function checkKasada() {
    return window.KPSDK ? true : false;
}
function checkAwsWaf() {
    return (window.AwsWafIntegration || document.cookie.includes('aws-waf-token')) ? true : false;
}
function checkIncapsula() {
    return (document.cookie.includes('incap_ses') || document.cookie.includes('reese84')) ? true : false;
}
function checkShapeF5() {
    if (location.href.includes('southwest.com')) {
        return true;
    }
    if (window.__xr_bmobdb) {
        return true;
    }
    const hasScript = [...document.scripts].some(script =>
        script.src && script.src.includes('--z=q') && script.src.includes('seed=')
    );
    
    // 检查 link 标签
    const hasLink = [...document.querySelectorAll('link')].some(link =>
        link.href && link.href.includes('--z=q') && link.href.includes('seed=')
    );
    // 检查 iframe 标签
    const hasIframe = [...document.querySelectorAll('iframe')].some(iframe =>
        iframe.src && iframe.src.includes('--z=q') && iframe.src.includes('seed=')
    );
    if( hasScript || hasLink || hasIframe){
        return true;
    }  
    return false;
}
function checkPerimeterX() {
    return window._pxAppId ? true : false;
}
checkRisk();