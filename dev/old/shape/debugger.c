#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <ctype.h>

#define MIN(a, b) (a > b ? b : a)

#define MEMORY_SIZE 65536
#define NUMBER_OF_REGISTERS 32
#define NUMBER_OF_COMMANDS 12
#define NUMBER_OF_INSTRUCTIONS 26
#define BUFFER_SIZE 300      
#define BREAKPOINTS_ARRAY_SIZE 100
                
char debugInstructions[][NUMBER_OF_COMMANDS] = {"list","stp","reg","mem","search","pc", "run", "q","--help","break","back","reset"};

enum opCodes {HALT, ADD, ADDI, SUB,SUBI,MUL,MULI,LW,SW,BEQ, BNE, BLT, BGT, BLE, 
                BGE, JMP, JR, JAL, OUT, DIV, DIVI, MOD, MODI, FACT, FACTI,SWAP};

struct Processor {
  uint32_t pc;
  int32_t gpr[NUMBER_OF_REGISTERS];
  uint8_t memory[MEMORY_SIZE]; 
};

//this is a global constant to store the state of the program, i.e. value 1 if program ran.
int programExitValue;

/*
  This method checks if the given tokenn is a register or not.
  @param token : specifes the token to be checked
  @return      : returns 1 if the given token is a register
*/
int checkRegister(char *token){
 return (token!=NULL) ? (token[0]=='$') : 0;
}

/*
  This method returns an integer value for the given register
  @param reg : specifes the reg whose int value has to be returned
  @return    : returns integer representation of the given string value 
               representation of the token
*/
int getRegisterNumber(char *reg){
  return atoi(reg+1);
}

/*
  This method checks if a given string is a number.
  @param num : points to the string to be checked
  @return    : returns 1 if true, 0 if false
*/

int checkIfNumber(char *num) {
  char *temp = num;
  while(*temp) {
    if (!isdigit(*temp)) return 0;
    temp++;
  }
  return 1;
}

/*
  This method prints an "invalid command" error.
  @param     : takes no parameters
  @return    : no return value
*/
void printInvalidCommandMessage(void) {
  printf("Invalid command. Please enter --help for help\n");
}

/*
  This method checks if all strings in the given array of strings are registers.
  @param regs : points to the array of strings to be checked
  @return     : returns 1 if all strings in the array are register names, 
                0 otherwise
*/
int checkAllRegistersAreValid(char **regs) {
  while (*regs) {
    if (!checkRegister(*regs) || !checkIfNumber(*regs+1) || 
              getRegisterNumber(*regs) <0 || 
              getRegisterNumber(*regs) >= NUMBER_OF_REGISTERS) {
      return 0;
    }
    regs++;
  }
  return 1;
}

/*
  This method returns the value stored in the specified register
  @param reg  : specifies the register index whose value has to be returned
  @param proc : specifies the processor from which the value of register has to
                be returned
  @return     : returns the value of the register specifed by the index given
*/
int32_t getRegisterValue(struct Processor *proc, int8_t reg){
  return proc->gpr[reg];
}

/*
  This method prints the registers according to the tokens received. The tokens 
  also contain print modifiers which specify any filters or parameters that the
  print should satisfy, e.g. "-r" to print through the range of registers that 
  follows.
  @param proc: specifies the processor from which the register values are to be
               returned
  @param num : points to the array of tokens to be used during the printing
               process
  @return    : no return value
*/
void printReg(struct Processor *proc , char **tokens) {
  int start = 0 ;
  int end = NUMBER_OF_REGISTERS-1;
  
  if (strcmp("-r",tokens[0])==0) {
    start = getRegisterNumber(tokens[1]);
    end   = getRegisterNumber(tokens[2]);
    tokens++;
    if(!start<end && !checkAllRegistersAreValid(tokens+1)){
      printInvalidCommandMessage();
      return;
    }
    if(tokens[2]!=NULL){
      printInvalidCommandMessage();
      return;
    }
  }
  else if (strcmp("-m",tokens[0])==0) {
    tokens++;
    if(!checkAllRegistersAreValid(tokens)){
      printInvalidCommandMessage();
      return;
    }
    int i =0;
    while(tokens[i]!=NULL) {
        printf("%s = %i \t",tokens[i],getRegisterValue(proc, getRegisterNumber(tokens[i])));
        i++;
      if (i%8==0) printf("      \n");
    }
    printf("\n (JVG)");
    return;    
  } 
  else if (!strcmp("-a",tokens[0])==0){
    printInvalidCommandMessage();
    return;
  } 
 int x=start;
 printf("%i,%i\n",x, end);
  for (int i=0; i<end%8 ; i++) {    
    for (int j=0;j<8 ; j++) {
      if(x>end) break;
      printf("$%i = %i \t",x,getRegisterValue(proc,x));
      x++;
    }
    printf("      \n");
  }  
}
/*
  This method searches the registers for values specified in the tokens 
  received. The tokens also contain search modifiers which specify any filters
  or parameters that the search should satisfy, e.g. "-r" to search through the
  range of registers that follows.
  @param proc   : specifies the processor from which the register values are to 
                  be obtained
  @param tokens : points to the array of tokens to be used during the printing
                  process
  @return       : no return value
*/
void searchRegisters(struct Processor *proc, char **tokens) {
  int start =0;
  int end = NUMBER_OF_REGISTERS-1;
  if (!checkIfNumber(tokens[1])) {
    printInvalidCommandMessage();
    return;
  }
  int value = atoi(tokens[1]);
  
  if (!checkAllRegistersAreValid(tokens+2)) {
    printInvalidCommandMessage();
    return;
  }
  
  if (strcmp(tokens[0],"-r")==0) {
    start = getRegisterNumber(tokens[2]);
    end = getRegisterNumber(tokens[3]);
    if (start>end) {
      printInvalidCommandMessage();
      return;
    }
    if (tokens[4]!=NULL) {
       printInvalidCommandMessage();
       return;
    }
  } else if (strcmp(tokens[0],"-a")!=0 || tokens[1]!=NULL) {
    printInvalidCommandMessage();
    return;
  }
  
  printf("\n(JVG)");
  for (int i = start; i<=end ; i++) {
    if (proc->gpr[i]==value) {
      printf("$%i=%i  ",i,value);
    }
  }
  printf("\n(JVG)");
}

/*
  This method checks if all strings in the given array of strings are names of 
  valid memory locations.
  @param regs : points to the array of strings to be checked
  @return     : returns 1 if all strings in the array are memory locations, 
                0 otherwise
*/
int checkIfAllMemoryLocationsAreValid(char **tokens) {
  while(*tokens) {
    if (!checkIfNumber(*tokens) || atoi(*tokens) <0 
                || atoi(*tokens)>=MEMORY_SIZE) return 0;
    tokens++;
  }
  return 1;
}
/*
  This method returns the data stored in the memory of the specifed processor
  at the specified address.
  @param proc    : specifies the processor 
  @param address : specifies the address of the memory which data has to be
                   fetched
  @return        : returns the value stored in the memory at the specified
                   address
*/
uint32_t getMemory(struct Processor *proc, uint32_t address) {
  return *(uint32_t *)(proc->memory + address);
}

/*
  This method prints the values memory locations according to the tokens 
  received. The tokens also contain print modifiers which specify any filters or
  parameters that the print should satisfy, e.g. "-r" to print through the
  range of memory locations that follows.
  @param proc: specifies the processor from which the memory values are to be
               returned
  @param num : points to the array of tokens to be used during the printing
               process
  @return    : no return value
*/
void printMemory(struct Processor *proc, char **tokens) {
  int start = 0;
  int end = MEMORY_SIZE-1;

  if ((strcmp(tokens[0],"-r"))==0) {
    start = atoi(tokens[1]);
    end = atoi(tokens[2]);
    tokens++;
    if (start>end) {
      printInvalidCommandMessage();
      return;
    }
    if (tokens[4]!=NULL) {
       printInvalidCommandMessage();
       return;
    }
  } else if ((strcmp(tokens[0],"-m"))==0) {
    int j=0;
    tokens++;
      if (!checkIfAllMemoryLocationsAreValid(tokens+1)) {
        printInvalidCommandMessage();
        return;
      }
    while (*tokens) {
      printf("M%i=%i  ",atoi(*tokens),getMemory(proc,atoi(*tokens)));
      tokens++;
      j++;
      if (j%8==0) printf("\n");
    }
    printf("\n (JVG)");
    return; 
  } else if ((strcmp(tokens[0],"-a"))!=0) {
    printInvalidCommandMessage();
    return;
  }
  int x= start;
  for (int c=0; x<end ; c++) {
    for (int d=0;d<8&&x<=end ;d++) {
      printf("M%i=%i \t",x,getMemory(proc,x));
      x++;
    }
    printf("\n");
  }
  
}

/*
  This method breaks up a given string into tokens which seperate register
  values, memory locations, search modifiers, etc
  @param command: specifies the string to be tokenised
  @return       : returns an array of strings which can be used as tokens
*/
char **tokeniseUserCommand(char *command) {
  char *buff = malloc(sizeof(char) * BUFFER_SIZE);
  buff = strncpy(buff,command,sizeof(char) *BUFFER_SIZE);
  char **tokens = malloc(sizeof(char) *BUFFER_SIZE);
  char *token = malloc(50);
  int i=0;
  token = strtok(buff," ");
  tokens[i] = token;
  while(token!=0) {
    i++;
    token = strtok(NULL," ");
    tokens[i] = token;
  }  
  return tokens;
}
/*
  This method searches the memory locations for values specified in the tokens 
  received. The tokens also contain search modifiers which specify any filters
  or parameters that the search should satisfy, e.g. "-r" to search through the
  range of memory locations that follows.
  @param proc   : specifies the processor from which the memory values are to 
                  be obtained
  @param tokens : points to the array of tokens to be used during the printing
                  process
  @return       : no return value
*/
void searchMemory(struct Processor *proc, char **tokens) {
  int start =0;
  int end = MEMORY_SIZE-1;
  if (!checkIfAllMemoryLocationsAreValid(tokens+1)) {
    printInvalidCommandMessage();
    return;
  }
  int value = atoi(tokens[1]);
  if (strcmp(tokens[0],"-r")==0) {
    start = atoi(tokens[2]);
    end = atoi(tokens[3]);
    if (start>end) {
      printInvalidCommandMessage();
      return;
    }
    if (tokens[4]!=NULL) {
       printInvalidCommandMessage();
       return;
    }
  } 
  else if (strcmp(tokens[0],"-a")!=0) {
    printInvalidCommandMessage();
    return;
  }
  printf("\n(JVG)");
  int x = start;
  for (int i = start; x<=end ; i++) {
    if (proc->memory[i]==value) {
      printf("M%i=%i\t",x,value);
    }
    if(i%8==0){
    printf("\n(JVG)");
    }
    x++;
   }
  printf("\n(JVG)");
}

/*
  This method begins the search process by checking if the tokens point towards
  a memory location or a register and calling the required method.
  @param proc   : specifies the processor to be passed as one of the arguments
                  to the functions called
  @param tokens : specifies the tokens to be used in the check
  @return       : no return value
*/
void search(struct Processor *proc,char **tokens) {
  if (strcmp(tokens[0],"-M") ==0) {
    printf("mem search\n");
    searchMemory(proc,tokens+1);
  } else if (strcmp(tokens[0],"-R")==0) {
    searchRegisters(proc,tokens+1);
  }
}

/*
  This method uses an array of integest to check if the line number specified is
  a break point. 
  @param breakPoints : points to the integers that indicate the breakpoints
  @param lineNumber  : specifies the line number
  @return            : returns 1 if the line number is a break point, 0 if not
*/
int checkIfBreakPoint(int *breakPoints, int lineNumber) {
  for (int i=0; i<BREAKPOINTS_ARRAY_SIZE ;i++) {
    if (breakPoints[i]==lineNumber) return 1;
    if (breakPoints[i]==-1) return 0;
    i++;
  }
  return 0;
}
/*
  This method prints the current value of the program counter(PC).
  @param proc : specifies the processor from which the PC value is to be 
                obtained
  @return     : no return value
*/
void printPC( struct Processor *proc) {
  printf("PC = %i \n",proc->pc);
}



/*
  This method returns the opcode (bit 0 to 5) from the given 32 bit instruction
  @param instruction : This specifies the 32 bit instruction
  @return            : The method returns 8bit representation of the opcode
*/
uint8_t getOpcode(uint32_t instruction) {
  uint32_t mask = 0xfc000000;
  uint32_t opcd = mask & instruction;
  opcd = opcd >> 26;
  uint8_t opCode = (int) opcd;
  return opCode;
}

/*
  This method returns the bit 6 to 31 of the given instruction, i.e. the address
  for j-type instructions
  @param instruction : this specifies the instruction
  @return            : the method returns 32 bit representation of the bit 6 to 
                       31 of the given instruction
*/
uint32_t getAddress(uint32_t instruction) {
  uint32_t mask = 0x03ffffff;
  return mask & instruction;
}

/*
  This method returns the bit 6 to 10 of the given instruction
  @param instruction : this specifies the instruction
  @return            : the method returns 8 bit representation of the bit 6 to 
                       10 of the given instruction
*/
uint8_t getR1(uint32_t instruction){
  uint32_t mask = 0x03e00000;
  uint32_t reg = mask & instruction;
  uint8_t r1 = reg>>21;
  return r1;

}

/*
  This method returns the bit 11 to 15 of the given instruction
  @param instruction : this specifies the instruction
  @return            : the method returns 8 bit representation of the bit 11 to 
                       15 of the given instruction
*/
uint8_t getR2(uint32_t instruction) {
  uint32_t mask = 0xf8000;
  uint32_t reg = mask & instruction;
  uint8_t r2 = reg >> 16;
  return r2;
}

/*
  This method returns the bit 16 to 21 of the given instruction
  @param instruction : this specifies the instruction
  @return            : the method returns 8 bit representation of the bit 16 to 
                       21 of the given instruction
*/
uint8_t getR3(uint32_t instruction) {
  uint32_t mask = 0x0007C00;
  return ((mask & instruction) >> 11);
}

/*
  This method returns the bit 16 to 31 of the given instruction
  @param instruction : this specifies the instruction
  @return            : the method returns 8 bit representation of the bit 16 to 
                       31 of the given instruction
*/
int16_t getImmediateValue(uint32_t instruction) {
  uint32_t mask = 0x0000ffff;
  return (int16_t)(mask & instruction);
}

/*
  This method sets the value of the memory at the specified addredd to the value
  given.
  @param proc    : specifies the processor
  @param address : specifies the address of memory which needs the value to be
                   set to the given value
  @param value   : specifies the new value for the memory to be set
*/
void setMemory(struct Processor *proc, uint32_t address, int32_t value) {
  *(uint32_t *)(proc->memory + address) = value;
}

/*
  This method returns the instruction stored in the memory at address specified
  by the program counter of the processor.
  @param proc : specifies the processor which contains the program counter,
                memory, and registers
*/
uint32_t getInstructionAtPC(struct Processor *proc){
  return *(uint32_t *)(proc->memory + proc->pc);
}

/*
  This method prints a segmentation fault error message.
  @param    : takes no parameters
  @return   : no return value
*/
void printSegmentationFaultMessage(void) {
  printf("Executing the current line would cause segmentation fault.\n");
  printf("Please use the 'list' command to track the line where the error occurred\n");
}

/*
  This method checks if the given instruction is a valid R-type instruction.
  @param ins  : this specifies the instruction
  @return     : 
*/
int checkRtypeInstructionIsValid(uint32_t ins) {
  uint8_t r1 = getR1(ins);
  uint8_t r2 = getR2(ins);
  uint8_t r3 = getR3(ins);
  if (r1<0 || r2<0 || r3<0 || r1>=NUMBER_OF_REGISTERS || r2>=NUMBER_OF_REGISTERS 
        || r3>=NUMBER_OF_REGISTERS) {
    printSegmentationFaultMessage();
    return 0;
  }
  return 1;
}

/*
  This method checks if the given instruction is a valid branch instruction. 
  @param ins  : specifies the instruction to be used for the check
  @param proc : specifies the processor which contains the values registers and 
                program counter
  @return     : returns 1 if the instruction is a valid branch instruction,
                0 if not
*/
int checkBranchInstructionIsValid(uint32_t ins, struct Processor *proc) {
  uint8_t r1 = getR1(ins);
  uint8_t r2 = getR2(ins);
  int16_t iVal = getImmediateValue(ins);
  uint32_t pc = proc->pc;
  if (r1<0 || r2<0 || r1>=NUMBER_OF_REGISTERS || r2>=NUMBER_OF_REGISTERS 
                                || pc+(iVal*4)<0 || pc+(iVal*4)>=MEMORY_SIZE) {
    printSegmentationFaultMessage();
    return 0;
  }
  return 1;
}

/*
  This method checks if the given instruction is a valid I-type instruction. 
  @param ins  : specifies the instruction to be used for the check
  @return     : returns 1 if the instruction is a valid I-type instruction,
                0 if not
*/
int checkItypeInstructionIsValid(uint32_t ins) {
  uint8_t r1 = getR1(ins);
  uint8_t r2 = getR2(ins);
  if (r1<0 || r2<0 || r1>=NUMBER_OF_REGISTERS || r2>=NUMBER_OF_REGISTERS) {
    printSegmentationFaultMessage();
    return 0;
  }
  return 1;
}

/*
  This method checks if the given instruction is a valid J-type instruction. 
  @param ins  : specifies the instruction to be used for the check
  @return     : returns 1 if the instruction is a valid J-type instruction,
                0 if not
*/
int checkJtypeIsValid(uint32_t ins) {
  uint32_t add = getAddress(ins);
  if (add<0 || add>=MEMORY_SIZE) {
    printSegmentationFaultMessage();
    return 0;
  }
  return 1;
}

/*
  This method checks if the given instruction is a valid "load" or "store" 
  instruction. 
  @param ins  : specifies the instruction to be used for the check
  @return     : returns 1 if the "load"/"store" instruction is valid, 0 if not
*/
int checkIfLoadAndStoreAreValid(uint32_t ins) {
  uint8_t r1 = getR1(ins);
  uint8_t r2 = getR2(ins);
  int16_t iVal = getImmediateValue(ins);
  if (r1<0 || r2<0 || r1>=NUMBER_OF_REGISTERS || r2>=NUMBER_OF_REGISTERS 
                                        || r2+iVal<0 || r2+iVal>=MEMORY_SIZE) {
    printSegmentationFaultMessage();
    return 0;
  }
  return 1;
}

/*
  This method checks if the current intruction is valid. 
  @param processor : specifies the processor which contains the value of the 
                     program counter
  @return          : returns 1 if the instruction at PC is a valid instruction,
                     0 if not
*/
int checkIfInstructionIsValid(struct Processor *processor) {
  uint32_t instruction = getInstructionAtPC(processor);
  uint8_t opcode = getOpcode(instruction);
  if (opcode<0 || opcode>NUMBER_OF_INSTRUCTIONS) {
    printf("The opcode for the current instruction is invalid. This would cause SEGMENTATION FAULT\n");
    programExitValue =1;
    return 0;    
  };
  switch (opcode)  {
    case HALT : return 1;
    case ADD  : return checkRtypeInstructionIsValid(instruction)!=0;
    case ADDI :return checkItypeInstructionIsValid(instruction)!=0;
    case SUB  : return checkRtypeInstructionIsValid(instruction)!=0;
    case SUBI : return checkItypeInstructionIsValid(instruction)!=0;
    case MUL  : return checkRtypeInstructionIsValid(instruction)!=0;
    case MULI : return checkItypeInstructionIsValid(instruction)!=0;
    case LW   : return checkIfLoadAndStoreAreValid(instruction)!=0; 
    case SW   : return checkIfLoadAndStoreAreValid(instruction)!=0;
    case BEQ  : return checkBranchInstructionIsValid(instruction,processor)!=0;
    case BNE  : return checkBranchInstructionIsValid(instruction,processor)!=0; 
    case BLT  : return checkBranchInstructionIsValid(instruction,processor)!=0;
    case BGT  : return checkBranchInstructionIsValid(instruction,processor)!=0;
    case BLE  : return checkBranchInstructionIsValid(instruction,processor)!=0;
    case BGE  : return checkBranchInstructionIsValid(instruction,processor)!=0;
    case JMP  : return checkJtypeIsValid(instruction)!=0;
    case JR   : return checkRtypeInstructionIsValid(instruction)!=0;
    case JAL  : return checkJtypeIsValid(instruction)!=0;
    case OUT  : return checkRtypeInstructionIsValid(instruction)!=0;
    case DIV  : return checkRtypeInstructionIsValid(instruction)!=0;
    case DIVI : return checkItypeInstructionIsValid(instruction)!=0;
    case MOD  : return checkRtypeInstructionIsValid(instruction)!=0;
    case MODI : return checkItypeInstructionIsValid(instruction)!=0;
    case FACT : return checkRtypeInstructionIsValid(instruction)!=0;
    case FACTI: return checkItypeInstructionIsValid(instruction)!=0;
    case SWAP : return checkRtypeInstructionIsValid(instruction)!=0;
    default   : return 0;
  }
}
/*
  This method carries out the instruction and returns the integer result of the 
  operation.
  @param processor : specifies the processor from which the instruction, 
                     register and program counter values are to be taken
  @return          : returns the integer that is the result of the operations
*/
int carryOutInstruction(struct Processor *processor) {
  uint32_t instruction = getInstructionAtPC(processor);
  uint8_t opcode = getOpcode(instruction);
  if (opcode<0 || opcode>NUMBER_OF_INSTRUCTIONS) {
    printf("The opcode for the current instruction is invalid. This would cause SEGMENTATION FAULT\n");
    programExitValue =1;
    return 0;    
  };
  uint32_t backupPC = processor->pc;
  int32_t temp;
  div_t division;
  switch (opcode)  {
    case HALT : return 0;
    case ADD  : if (checkRtypeInstructionIsValid(instruction)==0) return 0;
                processor->gpr[getR1(instruction)] = 
                  getRegisterValue(processor, getR2(instruction)) + 
                  getRegisterValue(processor, getR3(instruction));
                break;
                
    case ADDI : if (checkItypeInstructionIsValid(instruction)==0) return 0;
                processor->gpr[getR1(instruction)] = 
                  getRegisterValue(processor, getR2(instruction)) + 
                  getImmediateValue(instruction);
                break;
               
    case SUB  : if (checkRtypeInstructionIsValid(instruction)==0) return 0;
                processor->gpr[getR1(instruction)] = 
                  getRegisterValue(processor, getR2(instruction)) - 
                  getRegisterValue(processor, getR3(instruction));
                break;
                
    case SUBI : if (checkItypeInstructionIsValid(instruction)==0) return 0;
                processor->gpr[getR1(instruction)] = 
                  getRegisterValue(processor, getR2(instruction)) - 
                   getImmediateValue(instruction);
                 break;
                  
    case MUL  : if (checkRtypeInstructionIsValid(instruction)==0) return 0;
                processor->gpr[getR1(instruction)] = 
                  getRegisterValue(processor, getR2(instruction)) * 
                  getRegisterValue(processor, getR3(instruction));
                break;
                  
    case MULI : if (checkItypeInstructionIsValid(instruction)==0) return 0;
                processor->gpr[getR1(instruction)] = 
                  getRegisterValue(processor, getR2(instruction)) * 
                  getImmediateValue(instruction);
                break;
                
    case LW   : processor->gpr[getR1(instruction)] = 
                getMemory(processor, 
                          getRegisterValue(processor, getR2(instruction)) + 
                                            getImmediateValue(instruction));
                break;
                  
    case SW   : setMemory(processor, getRegisterValue
                  (processor, getR2(instruction)) + 
                  getImmediateValue(instruction), 
                  getRegisterValue(processor, getR1(instruction)));
                break;
                
    case BEQ  : if (checkBranchInstructionIsValid(instruction,processor)==0) 
                  return 0;
                if (processor->gpr[getR1(instruction)] == 
                    processor->gpr[getR2(instruction)]) 
                  { processor->pc += getImmediateValue(instruction) * 4;};
                break;
                  
    case BNE  : if (checkBranchInstructionIsValid(instruction,processor)==0) 
                return 0;
                if (processor->gpr[getR1(instruction)] != 
                    processor->gpr[getR2(instruction)]) 
                { processor->pc += getImmediateValue(instruction) * 4;};
                break;
                  
    case BLT  : if (checkBranchInstructionIsValid(instruction,processor)==0) 
                return 0;
                if (processor->gpr[getR1(instruction)] <
                   processor->gpr[getR2(instruction)])
                { processor->pc += getImmediateValue(instruction) * 4;};
                break;
                  
    case BGT  : if (checkBranchInstructionIsValid(instruction,processor)==0) 
                return 0;
                if (processor->gpr[getR1(instruction)] >
                  processor->gpr[getR2(instruction)]) 
                { processor->pc += getImmediateValue(instruction) * 4;};
                break;
                  
    case BLE  : if (checkBranchInstructionIsValid(instruction,processor)==0) 
                  return 0;
                if (processor->gpr[getR1(instruction)] <= 
                   processor->gpr[getR2(instruction)]) 
                { processor->pc += getImmediateValue(instruction) * 4;};
                break;
                  
    case BGE  : if (checkBranchInstructionIsValid(instruction,processor)==0) 
                return 0;
                if (processor->gpr[getR1(instruction)] >= 
                   processor->gpr[getR2(instruction)]) 
                { processor->pc += (getImmediateValue(instruction) * 4);};
                break;
                  
    case JMP  : if (checkJtypeIsValid(instruction)==0) return 0;
                processor->pc = getAddress(instruction);
                break;
                  
    case JR   : if (checkRtypeInstructionIsValid(instruction)==0) return 0;
                processor->pc = getRegisterValue
                  (processor, getR1(instruction));
                break;
                  
    case JAL  : if (checkJtypeIsValid(instruction)==0) return 0;
                processor->gpr[31] = processor->pc + sizeof(uint32_t); 
                processor->pc = getAddress(instruction);
                break;
                  
    case OUT  : if (checkRtypeInstructionIsValid(instruction)==0) return 0;
                printf("%c", (char)getRegisterValue
                  (processor, getR1(instruction)));
                break;
                  
    case DIV  : if (checkRtypeInstructionIsValid(instruction)==0) return 0;
                division = div(getRegisterValue(processor,getR2(instruction))
                            ,getRegisterValue(processor,getR3(instruction)));
                processor->gpr[getR1(instruction)] = division.quot;
     
    case DIVI : if (checkItypeInstructionIsValid(instruction)==0) return 0;
                division = div(getRegisterValue(processor,getR2(instruction))
                            ,getImmediateValue(instruction));
                processor->gpr[getR1(instruction)] = division.quot;
      
    case MOD  : if (checkRtypeInstructionIsValid(instruction)==0) return 0;
                division = div(getRegisterValue(processor,getR2(instruction))
                            ,getRegisterValue(processor,getR3(instruction)));
                processor->gpr[getR1(instruction)] = division.rem;
      
    case MODI : if (checkItypeInstructionIsValid(instruction)==0) return 0;
                division = div(getRegisterValue(processor,getR2(instruction))
                            ,getImmediateValue(instruction));
                processor->gpr[getR1(instruction)] = division.rem;
      
    case FACT : if (checkRtypeInstructionIsValid(instruction)==0) return 0;
                processor->gpr[getR1(instruction)] = 
                getRegisterValue(processor, getR2(instruction));
                for(int i = 1; i<processor->gpr[getR2(instruction)] ; i++) {
                  processor->gpr[getR1(instruction)] = 
                    (getRegisterValue(processor, getR1(instruction)))*
                    (getRegisterValue(processor, getR2(instruction))-i);
                }
                break;
      
    case FACTI: if (checkItypeInstructionIsValid(instruction)==0) return 0;
                processor->gpr[getR1(instruction)] = 
                getImmediateValue(instruction);
                for(int i = 1; i<getImmediateValue(instruction) ; i++) {
                  processor->gpr[getR1(instruction)] = 
                    (getRegisterValue(processor, getR1(instruction)))*
                    (getImmediateValue(instruction)-i);
                }
                break;
      
    case SWAP : if (checkRtypeInstructionIsValid(instruction)==0) return 0;
                temp = 
                  getRegisterValue(processor, getR1(instruction));
                processor->gpr[getR1(instruction)] = 
                  getRegisterValue(processor, getR2(instruction));
                processor->gpr[getR2(instruction)] = temp;
                break;
  }
  if(processor->pc == backupPC)  processor->pc += sizeof(uint32_t);
  return 1;
}

/*this method carries out one step 
@param  : current state of the processor
@return : a string without the white spaces in it
*/
void step(struct Processor *proc) {
  if (programExitValue==1) {
    printf("No programs running currently. The previous program has exited already so step cannot be executed\n");
    return;
  }
  int retVal = carryOutInstruction(proc);
  if (retVal==0) {
    programExitValue= 1;
    printf("\n\nProgram exited normally.\n");
  }
}
/*This method removes the space in a string
@param str : a string which has white space in it
@return : a string without the white spaces in it
*/
char *removeSpace(char *str) {
  while(*str) {
    if (isspace((int) *str)==0) return str;
    str++;
  }
  return str;
}

/*
  The method binaryFileLoader loads the binary file in the memory of the given
  processor.
  @param processor : this specifes the current processor with the memory to be
                     initialised with the given instructions from given filepath
  @param filepath  : this specifies the path of the file which contains the
                     instructions to be loaded in the memory.
*/
void binaryFileLoader(char *filepath, struct Processor *processor) {
  FILE *fp;
  fp = fopen(filepath,"rb");
  if (fp==NULL) {
    perror("ERROR in opening file");
    exit(EXIT_FAILURE);
  }

  int fileSize;
  
  fseek (fp , 0 , SEEK_END);
  fileSize = ftell (fp);
  rewind (fp);

  fileSize = MIN(65536, fileSize);

  fread(processor->memory, sizeof(uint32_t), fileSize, fp);
  fclose(fp);
}
/* this method is used to get the specific line from the input file
@param filepath : the path to the file to be searched
@param n        : the line number to be retrieved
@return         : returns no specific value however prints out the line if it 
                  exist or prints End of file reached before line

*/
void listInstruction(char *filepath, int n) {
  FILE *fp;
  fp = fopen(filepath,"r");
  char *buffer = (char *) malloc(BUFFER_SIZE * sizeof(char));
  if (fp==NULL) {
    perror("ERROR in opening file");
    exit(EXIT_FAILURE);
  }
  while (!feof(fp) &&0<n ){
    memset(buffer, 0, ((sizeof(char))*BUFFER_SIZE));
    fgets (buffer, BUFFER_SIZE, fp); 
    if(strlen(buffer)>1) n--;
    //printf("%s------n=%i----length =%i\n", buffer,n,strlen(buffer));
    
  }
  if(n==0) {
    printf("%s", removeSpace(buffer));
  }
  else{
    perror("End of file reached before line");
  }                  
  free(buffer);
  fclose(fp);
}



/*
  This method prints the state of the processor at the end of execution of the
  program; i.e. the data stored in all the registers and the value of program
  counter at the end of the program
  @param proc : this specifies the processor whose state has to be printed
*/
void dumpProcessor(struct Processor *proc) {
  fprintf(stderr, "\n\n-----\n\nPC=%d\n", proc->pc);
  for(int i = 0; i < 4; i++) {
    for(int j = 0; j < 8; j++) {
       int reg = i * 8 + j;
       fprintf(stderr, "R%d=%d\t", reg, getRegisterValue(proc, reg));
    }
      fprintf(stderr, "\n");
   }
}
/*
  This method prints out the Welcome message at the at the start of the 
  of the program.
  @param   :Takes no parameters
  @return  :Returns no values
*/
void printWelcomeMessage(void){
  FILE *fp;
  fp = fopen("welcomeMessage.txt","r");
  char *buffer = (char *) malloc(BUFFER_SIZE * sizeof(char));
  if (fp==NULL) {
    perror("ERROR in opening file");
    exit(EXIT_FAILURE);
  }
  while (!feof(fp)){
    memset(buffer, 0, ((sizeof(char))*BUFFER_SIZE));
    fgets (buffer, BUFFER_SIZE, fp); 
    printf("%s",buffer);    
  }
}
/*
  This method checks whether the user has inputted the right commands for 
  the program.
  @param  command: specifies the command to be used in the check
  @return        : returns 1 if the command is valid and 0 if not
*/
int checkUserCommandIsValid(char *command) {
  for (int i=0; i<NUMBER_OF_COMMANDS; i++) {
    if (strcmp(command,debugInstructions[i])==0) return 1;
  }
  return 0;
}
/*
  This is a method to get a command from the user. Endlessly loops to 
  continuously get commands from the user until program is quit.
  @param  : Takes no parameters
  @return : Returns an array of strings that the user types into the debugger
            that seem like valid commands
*/
char **getUserCommand(void) {
  printf("(JVG)");
  char *buff = malloc(BUFFER_SIZE);
  fgets(buff,BUFFER_SIZE,stdin);
  char *ptr = malloc(2);
  if( (ptr = strchr(buff, '\n')) != NULL) *ptr = '\0';
  char **tokens = malloc(sizeof(char) * BUFFER_SIZE);
  tokens = tokeniseUserCommand(buff);
  if (checkUserCommandIsValid(tokens[0])) return tokens;
  printInvalidCommandMessage();
  return getUserCommand();
}

/*
  This is a method to get confirmation from the user of quitting the 
  program 
  @param  :Takes no parameters
  @return :returns 1 if the user wants to quit or 0 otherwise
*/
int confirmToQuit(void) {
  printf("Are you sure you want to quit? enter y for yes and n for no\n(JVG)");
  char *ans = malloc(sizeof(char) * BUFFER_SIZE);
  fgets(ans,sizeof(char) * BUFFER_SIZE, stdin);
  char *ptr = ans;
  if( (ptr = strchr(ans, '\n')) != NULL) *ptr = '\0';
  int ret = strcmp(ans,"y")==0;
  if (ret==0 && strcmp(ans,"n")!=0) {
    free(ans);
    printf("Please enter a valid answer\n");
    return confirmToQuit();
  } 
  free(ans);
  return ret;
}
 
 /*
  Runs the piece of code from the current step.
  @param proc        : specifies the processor containing the PC values
  @param breakPoints : specifies the break points to be checked for in the lines
                       of code.
  @return            : no return value.
 */
void run(struct Processor *proc,int *breakPoints) {
  if (programExitValue==1) {
      printf("No programs running currently. The previous program has exited already so step cannot be executed\n");
      return;
  }
  int retVal = 1;
  
  do {
    retVal = carryOutInstruction(proc);  
  } while (retVal && !checkIfBreakPoint(breakPoints,(proc->pc/4)+1));
  if (programExitValue==1) return;
  if (checkIfBreakPoint(breakPoints,((int) proc->pc/4)+1)==1) {
    printf("Breakpoint reached.\n");
    return;
  }
  fflush(stdout);
  dumpProcessor(proc);
  programExitValue = 1;
  printf("\nProgram exited normally.\n");
}

/*
  This method sets a breakpoint at every occurance of a breakpoint in the given 
  tokens. 
  @param breakPoints : specifies the line numbers to be used as break points
  @param tokens      : specifies the array of strings to be used as the tokens 
                       that need to be checked for numbers
  @return            : no return value
*/
void setBreakPoints(int *breakPoints,char **tokens) {
  int i=0;
  if (strcmp(tokens[0],"-r")==0) {
    tokens++;
    while(*tokens) {
      if (checkIfNumber(*tokens)==0) {
        printInvalidCommandMessage();
        return;
      }
      if (breakPoints[i]==atoi(*tokens)) {
        breakPoints[i] = -1;
      };
      if (breakPoints[i] ==-1) {
        printInvalidCommandMessage();
        printf("breakpoint does not exists");
        return;
      }
      i++;
      tokens++;
    }
  } else if (strcmp(tokens[0],"-a")==0) {
    tokens++;
    int *temp = malloc(sizeof(int) * BREAKPOINTS_ARRAY_SIZE);
    while(*tokens) {
      if (checkIfNumber(*tokens)==0) {
        printInvalidCommandMessage();
        return;
      }
      temp[i] = atoi(*tokens);
      i++;
      tokens++;
    }
    memcpy(breakPoints,temp,sizeof(int) * i);
    free(temp);
  }
}

/*
  This method is used to reset the state of the cpu to the state it would
  have been in at the start of the program.
  @param proc :specifes the current state of the cpu
  @param bin  :specifies the filepath of the binary path
*/
void reset(struct Processor *proc,char *bin) {
  memset(proc,0,sizeof(struct Processor));
  binaryFileLoader(bin,proc);
  programExitValue = 0;
}

/*
  This method displays the help content in the terminal for the user to get help
  @param tokens : specifies the tokens of the given command for help 
*/
void help(char **tokens){
  if(tokens[1]!=NULL){
    if(strcmp(tokens[1],"mem") ==0){
      system("cat help/mem.txt");
      return;
    }
    else if(strcmp(tokens[1],"reg") ==0){
     system("cat help/reg.txt");
     return;
    }    
    else if(strcmp(tokens[1],"search") ==0){
     system("cat help/search.txt");
     return;
    }   
  }
  system("cat help/help.txt");
}

/*
  This method is used to execute the user command.
  @param assembly    : specifies the assembly instruction to be used
  @param bin         : specifies the binary code to be used
  @param proc        : specifies the processor that contains the values used
  @param tokens      : specifies the tokens to be used to execute the command
  @param breakPoints : specifies the various line numbers to be used as break 
                       points
  @return            : returns 0 when executing any command except confirmation
                       of the quit command
*/
int executeUserCommand(char *assembly, char *bin, struct Processor *proc, 
                        char **tokens, int *breakPoints) {
  if (strcmp(tokens[0], "reg")==0) {
    tokens++;
    printReg(proc, tokens);
    return 0;
  } else if (strcmp(tokens[0], "mem")==0) {
    tokens++;
    printMemory(proc, tokens);
    return 0;
  } else if (strcmp(tokens[0], "pc")==0) {
    printPC(proc);
    return 0;
  } else if (strcmp(tokens[0], "search")==0) {
    tokens++;
    search(proc, tokens);
    return 0;
  } else if (strcmp(tokens[0], "stp")==0) {
    step(proc);
    return 0;
  } else if (strcmp(tokens[0], "list")==0) {
    listInstruction(assembly, ((proc->pc)/4)+1);
    return 0;
  } else if (strcmp(tokens[0], "--help")==0) {
    help(tokens);
    return 0;
  } else if (strcmp(tokens[0], "run")==0) {
    run(proc,breakPoints);
    return 0;
  } else if (strcmp(tokens[0],"q")==0) {
    return confirmToQuit();
  } else if (strcmp(tokens[0],"break")==0) {
    setBreakPoints(breakPoints,tokens+1);
    return 0;
  } else if(strcmp(tokens[0],"reset")==0) {
    reset(proc,bin);
    return 0;
  }
  return 0;
}

int main(int argc, char **argv) {
  struct Processor *proc = malloc(sizeof(struct Processor));
  assert("There are wrong number of arguents given" && argc==3);
  char *fBin = argv[2];
  char *fAssembly = argv[1];
  memset(proc,0,sizeof(struct Processor));
  binaryFileLoader(fBin,proc);
  system("clear");
  int *breakPoints = malloc(sizeof(int) *BREAKPOINTS_ARRAY_SIZE);
  memset(breakPoints,-1,sizeof(int) *BREAKPOINTS_ARRAY_SIZE);
  printWelcomeMessage();
  char **tokens = malloc(sizeof(char) *BUFFER_SIZE);
  int returnVal = 0; 
  do {
    tokens = getUserCommand();
    returnVal = executeUserCommand(fAssembly,fBin,proc,tokens,breakPoints);
    free(tokens);
  } while (!returnVal);
  printf("Thanks for using JVG debugger\n");
  system("clear");
  free(proc);
  free(breakPoints);
  return EXIT_SUCCESS;
}
