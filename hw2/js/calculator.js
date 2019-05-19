/**
 * var newValue to record new value each time.
 */
var newValue = 0;
/**
 * var newValue to record previous value.
 */
var preValue = 0;
/**
 * var preOp to record previous operation.
 */
var preOp = "+";
/**
 * Boolean flag to judge whether click two or more operations continuously
 */
var flag = false;
/**
 * Update digit value when click digit button.
 * @param value 
 */
function setValue(value){
    //if calculate after "=", then reset;
    if(preOp ==="="){
        preOp="+";
        preValue=0;
    }
    flag = true;
    newValue = newValue*10 + value;
    document.getElementById("calc-display").value=newValue;
}
/**
 * Update operation and calculate result based on operation.
 * @param op 
 */
function setOp(op){
    //if click two operations continously,then calculate based on the last operation
    if(flag == false) {
        return preOp = op;
    }
    var re;

    if(preOp ==="+") re = preValue+newValue;
    if(preOp ==="-") re = preValue-newValue;
    if(preOp ==="*") re = preValue*newValue;
    if(preOp ==="/") {
        //if divide by 0, alert and reset;

        if(newValue ==0){
            alert("Can not divide by zero");
            document.getElementById("calc-display").value= 0;
            newValue = 0;
            preValue = 0;
            preOp = "+";
            return;
            
        }else{
            re = (parseInt) (preValue/newValue);
        }
        
    }
    document.getElementById("calc-display").value= re;
    preValue = re;
    newValue = 0;
    preOp = op;
    flag = false;
}
