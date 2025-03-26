parser grammar RiddleParser;

options {
    tokenVocab=RiddleLexer;
}

@Header{

}

@parserFile::members {
}



program
    : statement_ed*
    | EOF
    ;
    
null_cnt
    : Semi
    | Endl
    ;

statement_ed
    : statement Semi? Endl?
    | Semi
    | Endl
    ;

statement
    : packStatement
    | importStatement
    | classDefine
    | funcDefine
    | varDefineStatement
    | forStatement
    | whileStatement
    | ifStatement
    | returnStatement
    | continueStatement
    | breakStatement
    | tryExpr
    | expression
    | bodyExpr
    ;

bodyExpr
    : LeftCurly statement_ed* RightCurly
    ;

packStatement
    : Package packName=id
    ;

importStatement
    : Import libName=id
    ;

varDefineStatement
    : Var name=id Colon type=typeUsed
    | Var name=id Assign value=expression
    | Var name=id Colon type=typeUsed Assign value=expression
    ;

argsExpr
    : ((expression Comma)* expression)?
    ;

defineArgs returns [bool varArg]
    : ((id Colon typeUsed Comma)* (id Colon typeUsed))? {$varArg=False}
    | ((id Colon typeUsed Comma)* (id Colon typeUsed)) (Comma Dot Dot Dot) {$varArg=True}
    | (Dot Dot Dot) {$varArg=True}
    ;

funcDefine
    : (prop=property)? Endl? (tmpl=tmpleDefine)? Endl? mod=modifierList Func funcName=id LeftBracket args=defineArgs RightBracket (Sub Greater returnType=typeUsed)? ((body=bodyExpr)|Semi)
    ;

forStatement
    : For LeftBracket (init=statement)? Semi (cond=statement)? Semi (incr=statement)? RightBracket body=statement_ed
    ;

whileStatement
    : While LeftBracket cond=expression RightBracket body=statement_ed
    ;

continueStatement
    : Continue
    ;

breakStatement
    : Break
    ;

ifStatement returns [bool hasElse]
    : If LeftBracket cond=expression RightBracket body=statement_ed {$hasElse=False}
    | If LeftBracket cond=expression RightBracket body=statement_ed Else elseBody=statement_ed {$hasElse=True}
    ;

returnStatement
    : Return (result=statement)?
    ;

classDefine
    : (prop=property)? Endl? (tmpl=tmpleDefine)? Endl? Class className = id (Colon parentClass=id)? body=bodyExpr
    ;

tryExpr
    : Try tryBody=bodyExpr null_cnt? catchExpr
    ;

catchExpr
    : Catch LeftBracket varDefineStatement RightBracket
    ;

// 这一块就是使用
exprPtr
    : funcName=id (tmpl=tmplUsed)? LeftBracket args=argsExpr RightBracket    #funcExpr
    | id                                                                     #objectExpr
    | parentNode=exprPtr Dot childNode=exprPtr                               #blendExpr
    ;

exprPtrParser
    : exprPtr
    ;

expression
    : Less type=typeUsed Greater LeftBracket value=exprPtrParser RightBracket #castExpr
    | LeftBracket expr=expression RightBracket              #bracketExpr    // (x)
    | Not expr=expression                                   #notExpr        // !x
    | Add expr=expression                                   #positiveExpr   // +x
    | Sub expr=expression                                   #negativeExpr   // -x
    | Add Add expr=exprPtrParser                                  #selfAddLeftExpr // ++x
    | expr=exprPtrParser Add Add                                  #selfAddRightExpr // x++
    | Sub Sub expr=exprPtrParser                                  #selfSubLeftExpr // ++x
    | expr=exprPtrParser Sub Sub                               #selfSubRightExpr // x++
    | exprPtr                                               #ptrExpr
    | left=expression Star right=expression                 #mulExpr        // x*y
    | left=expression Div  right=expression                 #divExpr        // x/y
    | left=expression Mod right=expression                  #modExpr        // x%y
    | left=expression Add right=expression                  #addExpr        // x+y
    | left=expression Sub right=expression                  #subExpr        // x-y
    | left=expression LeftLeft right=expression             #shlExpr        // x<<y
    | left=expression RightRight right=expression           #aShrExpr  // x>>y
    | left=expression RightRightRight right=expression      #lShrExpr  // x>>>y
    | left=expression Greater right=expression              #greaterExpr    // x>y
    | left=expression Less   right=expression               #lessExpr       // x<y
    | left=expression Greater Assign right=expression       #greaterEqualExpr // x>=y
    | left=expression Less Assign right=expression          #lessEqualExpr  // x<=y
    | left=expression Equal  right=expression               #equalExpr      // x==y
    | left=expression Not Assign right=expression           #notEqualExpr   // x!=y
    | left=expression And right=expression                  #bitAndExpr     // x&y
    | left=expression Xor right=expression                  #bitXorExpr     // x^y
    | left=expression Or right=expression                   #bitOrExpr      // x|y
    | left=expression And And right=expression              #andExpr        // x&&y
    | left=expression Or Or right=expression                #orExpr         // x||y
    | left=exprPtrParser Assign right=expression               #assignExpr     // x=y
    | left=exprPtrParser Add Assign right=expression           #addAssignExpr     // x+=y
    | left=exprPtrParser Sub Assign right=expression           #subAssignExpr     // x-=y
    | left=exprPtrParser Star Assign right=expression          #mulAssignExpr    // x*=y
    | left=exprPtrParser Div Assign right=expression           #divAssignExpr     // x/=y
    | left=exprPtrParser Mod Assign right=expression           #modAssignExpr     // x%=y
    | left=exprPtrParser Add Assign right=expression           #addAssignExpr     // x+=y
    | left=exprPtrParser And Assign right=expression           #andAssignExpr          // x&=y
    | left=exprPtrParser Or  Assign right=expression           #orAssignExpr           // x|=y
    | left=exprPtrParser Xor Assign right=expression           #xorAssignExpr          // x^=y
    | left=exprPtrParser LeftLeft Assign right=expression      #shlAssignExpr     // x<<=y
    | left=exprPtrParser RightRight Assign right=expression    #aShrAssignExpr   // x>>=y
    | left=exprPtrParser RightRightRight Assign right=expression    #lShrAssignExpr   // x>>>=y
    | parentNode=expression Dot childNode=exprPtr           #exprBlend  // 新增此规则
    | Star expr=expression                                  #loadExpr   // 解引用
    | STRING                                                #stringExpr
    | CHAR                                                  #charExpr
    | number                                                #numberExpr
    | boolean                                               #booleanExpr
    | Null                                                  #nullExpr
    ;

id: Identifier;

// 修饰符
modifier
    : Public
    | Protected
    | Private
    | Operator
    | Virtual
    | Static
    | Override
    ;

modifierList
    : modifier*
    ;

//这里是指字面量
number
    : integer
    | float
    ;

boolean returns [bool value]
    : True_ {$value=True}
    | False_ {$value=True}
    ;

float returns [double value]
    : Float{$value = float($Float.text);}
    ;

integer returns [int value]
    : Decimal{$value = int($Decimal.text);}
    | Hexadecimal{$value = int($Hexadecimal.text.substr(2),16);}
    | Binary{$value = int($Binary.text.substr(2),2);}
    | Octal{$value = int($Octal.text.substr(1),8);}
    ;

tmpleDefine
    : Template Less tmplDefineArg (Comma tmplDefineArg)* Greater
    ;

tmplDefineArg
    : TypeName name=id // 表示一个 类型
    | typeUsed name=id // 表示一个 常量
    ;

tmplUsed
    : Less args=tmplArgList Greater
    ;

tmplArg
    : expression
    | typeUsed
    ;

tmplArgList
    : ((tmplArg Comma)* tmplArg)?
    ;

typeUsed
    : name=exprPtr Star*                                            #baseType      // 普通名称
    | name=exprPtr tmpl=tmplUsed                                    #tmplType      // 模板
    | baseType=typeUsed LeftSquare size=expression RightSquare      #arrayType     // 数组
    ;

property
    : LeftSquare LeftSquare propertyItem (Comma propertyItem)* RightSquare RightSquare
    ;

propertyItem
    : Identifier
    ;