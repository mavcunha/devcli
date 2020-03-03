#!/usr/bin/env bash
declare -r MAIN_COMMAND_VERSION="1.1"
declare -r MAIN_COMMAND=$(basename ${0})
declare -r ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd)"
declare -r PROJECTS_DIR="$(cd ${ROOT_DIR}/.. && pwd)"

# color output functions
function _color()     { tput -Txterm setaf ${1}; echo -ne ${2}; tput -Txterm sgr0; }
function in_red()     { _color 1 "${1}"; } # use for failures
function in_green()   { _color 2 "${1}"; } # use for successes
function in_yellow()  { _color 3 "${1}"; } # use for warnings / attention
function in_magenta() { _color 5 "${1}"; } # use for debug messages
function in_cyan()    { _color 6 "${1}"; } # use for main actions / progress

function __box() {
  echo "$(in_cyan '[')$(echo "${1}" )$(in_cyan ']')"
}

function red_box()     { __box "$(in_red "${1}")";     }
function green_box()   { __box "$(in_green "${1}")";   }
function yellow_box()  { __box "$(in_yellow "${1}")";  }
function magenta_box() { __box "$(in_magenta "${1}")"; }

# This is a simple formatting function which helps
# to create listing outputs such as:
# ENTRY....................RESULT
# ENTRY2...................RESULT2
#
function with_dots_between() {
  local entry="${1}"
  local result="${2}"
  local ndots="${3:-25}"
  log "with_dots_between: ndots=${ndots}"

  sep=$(printf ".%.0s" {1..25}) # large sequence of '.' for formatting

  printf "%s%s%s\n" "${entry}" "${sep:${#entry}}" "${result}"
}

# This is a shortcut for exiting with error
# calling error will stop the script
function error() {
  # error MSG - show error message in the form of "ERROR: MSG" and exit
  in_red "ERROR: ${1}\n"
  exit 1
}

# This is a shortcut for warning messages,
# these won't stop the execution of the script
function warn() {
  # warn MSG - show a warning in the form of "WARN: MSG"
  in_yellow "WARN: ${1}\n"
}

# stop on outdated bash
[[ ${BASH_VERSION%%.*} -lt 4 ]] \
  && error "Outdated bash version (${BASH_VERSION}), \
  use bash 4 or newer to run ${MAIN_COMMAND}"


# will evaluate if there's a env variable in the
# form of MAIN_COMMAND_SUFFIX, if defined
# will return its value otherwise default
# will be returned.
# This is not the same as ${VAR:-DEFAULT} because
# VAR is dynamic. If the command line gets renamed
# these are supposed to keep working regarless
function dyn_value() {
  # dyn_value SUFFIX DEFAULT - returns env variable value MAIN_COMMAND + _SUFFIX or DEFAULT
  local suffix="${1}"
  local default="${2}"
  local varname="${MAIN_COMMAND^^}_${suffix}"
  log "${varname}='${!varname}' || '${default}'"
  echo ${!varname-${default}}
}

# log functions should be defined as soon as possible
# so it become available for other functions
# because of the 'tput' calls on and off to
# change the debug message color there's
# a performance penalty on heavy logging
function log() {
  # log MSG - logs a message when debug is enabled
  if [[ -n ${DEBUG} ]]; then
    tput -Txterm setaf 5 >&2
    echo -e "debug: ${*}" >&2
    tput -Txterm sgr0 >&2
  fi
}

# flag for debug messages, it can be defined using
# and environment variable or using the --debug flag
DEBUG=$(dyn_value "DEBUG" "")

# Variables that can be overridden by the environment:
# TOOL_WORKING_DIR is a shortcut for tool/conf and tool/tool.d
# CONFIGURATION_DIR points to where "load_conf" will look
# SUBCOMMANDS_DIR is the main dir where commands are load from
# Using TOOL_WORKING_DIR where TOOL is the name of the tool
# is preferred
function handle_environment() {
  local command="${1}"
  log "handling environment variables for ${command}"

  local workdir="${command^^}_WORKING_DIR"
  log "${workdir}=${!workdir}"

  local tool_root_dir=${!workdir-${ROOT_DIR}}

  declare -gr CONFIGURATION_DIR=$(dyn_value "CONF_DIR" "${tool_root_dir}/conf")
  declare -gr SUBCOMMANDS_DIR=$(dyn_value "SUBCMD_DIR" "${tool_root_dir}/${command}.d")

  log "CONFIGURATION_DIR=${CONFIGURATION_DIR}"
  log "SUBCOMMANDS_DIR=${SUBCOMMANDS_DIR}"
}
handle_environment "${MAIN_COMMAND}"


function use() {
  # use LIB - loads library LIB in the current context
  local lib="${SUBCOMMANDS_DIR}/_${1}"
  log "requiring library: ${lib}"
  [[ -f ${lib} ]] && source ${lib} || error "Library '${lib}' not found"
}

function load_conf() {
  # load_conf CONF - loads conf/CONF file, see 'docs loadconf'
  local section="${1}"
  log "loading configuration for: ${section}"
  # this will declare ${section} as a global assoc array
  # which can be used anywhere.
  log "declaring ${section} as global associative array"
  declare -Ag "${section}"
  if __no_subcmd; then
    local conf="${CONFIGURATION_DIR}/${section}"
    log "loading global configuration: ${conf}, if missing won't fail."
    [[ -f ${conf} ]] && source "${conf}"
  else
    local conf="${CONFIGURATION_DIR}/${SUBCOMMAND}/${section}"
    log "loading subcommand configuration: ${conf}, if missing will fail."
    [[ -f ${conf} ]] && source "${conf}" \
      || error "Configuration '${conf}' not found"
  fi
  log "loaded ${section} as '$(__assoc_array_to_string ${section})'"
  # the assoc array is protected to avoid changes
  # in these configurations after they are loaded
  # just to avoid confusion
  readonly "${section}"
}

# loads file pointed by cmdmap key
# if ['SUBCOMMAND']='FILE' in cmdmap it will
# load 'FILE' iff the command if SUBCOMMAND is being
# called. This function allows for loading different
# implementations for the same SUBCOMMAND, example:
#
# 'pass' can be handled by keychain or password-store
#
function handle_interface() {
  # handle_interface ${@} - calls subcommand using function, see: 'docs cmdmap'
  __no_subcmd && return

  log "handling interface for '${SUBCOMMAND}'"
  use "${cmdmap[${SUBCOMMAND}]:-empty}" \
    || error "can't load implementation for '${SUBCOMMAND}'"

  log "forwarding call '${@}' to implementation '${cmdmap[${SUBCOMMAND}]}'"
  log "calling: cmd:${1:-"false"} args:${@:2}"
  [[ -n ${1} ]] && ${SUBCOMMAND}_${1:-"false"} ${@:2}
}

# add itself to PATH if needed
log "check if ${MAIN_COMMAND} is on PATH"
type -a ${MAIN_COMMAND} &> /dev/null
if [[ $? -ne 0 ]]; then
  log "exporting ${MAIN_COMMAND} to PATH"
  export PATH=${PATH}:${ROOT_DIR}
fi

# environment settings that depend on a project
[[ -f ${SUBCOMMANDS_DIR}/_environment ]] && . ${SUBCOMMANDS_DIR}/_environment

# evaluate if we have been called with a subcommand
# like 'MAIN_COMMAND SUBCMD' or just 'MAIN_COMMAND'
function __no_subcmd() {
  # __no_subcmd - returns if a subcommand was given or not
  log "called __no_subcmd()"
  [[ -z ${SUBCOMMAND} ]]
}

# util function to output assoc arrays
function __assoc_array_to_string() {
  # __assoc_array_to_string - returns an assoc array as a string for log output
  local -n assoc_array="${1}"
  for k in ${!assoc_array[@]}; do
    values="${values}[${k}]=${assoc_array[${k}]} "
  done
  echo "${values}"
}

###############################################################
# subcommand mapping
# load any mapping between subcommands
# and implementations, see: conf/cmdmap
load_conf cmdmap
###############################################################

# Lists all subcommands ignoring those with a leading "_"
# which are libraries
function _list_commands() {
  # _list_commands - lists all subcommands and ignore libraries
  cat <<EOU
  usage: ${MAIN_COMMAND} [-h|-?|--help|help] [-l|--libs] [--version] [--debug] [SUBCOMMAND]

  -h|-?|--help|help            Show this help message

  -l|--libs                    List available libraries

  --version                    Display current version

  --debug                      Will turn debug mode on. The same can be achieved by
                               setting ${MAIN_COMMAND^^}_DEBUG=true

  Subcommands available ('${MAIN_COMMAND} SUBCOMMAND' for usage):

EOU
  log "reading subcommands from ${SUBCOMMANDS_DIR}"
  for i in $(export LC_COLLATE=C; find ${SUBCOMMANDS_DIR} -maxdepth 1 -type f -or -type l | grep -vE '/_[^[:blank:]]+$' | sort); do
    source "${i}"
    local libname=$(basename ${i})
    printf "  %.24s %-60s\n" \
       "${libname}                                          " \
       "${SUBCOMMAND_DESC}"
  done
  echo
  exit 1
}

function _list_libraries() {
  # _list_libraries - list all libraries and ignore subcommands
  cat <<EOU

  Libraries available ('${MAIN_COMMAND} LIBRARY' for more information):

EOU
  log "reading libraries from ${SUBCOMMANDS_DIR}"
  for i in $(export LC_COLLATE=C; ls ${SUBCOMMANDS_DIR}/* | grep -E '/_[^[:blank:]]+$' | sort); do
    source "${i}"
    local libname=$(basename ${i})
    printf "  %.24s %-60s\n" \
       "${libname}                                          " \
       "${SUBCOMMAND_DESC}"
  done
  echo
  exit 1
}

function _subcommand_help() {
  # _subcommand_help - display SUBCOMMAND_HELP defined in subcommands
  local subcmd=${1}
  local subhelp=${2}
  cat <<EOU

  Showing '${MAIN_COMMAND} ${subcmd}' available actions:

  ${subhelp}

EOU
  exit 1
}

function _help() {
  # _help - display current subcommand help
  _subcommand_help ${SUBCOMMAND} "${SUBCOMMAND_HELP}"
}

function _handle_subcommand() {
  # _handle_subcommand - if args are given call subcommand if not call for help
  local -r SUBCOMMAND=${1}; shift 1
  local -r ACTION="${@}"

  log "running ${SUBCOMMANDS_DIR}/${SUBCOMMAND} ${ACTION} "
  . "${SUBCOMMANDS_DIR}/${SUBCOMMAND}" ${ACTION}

  if [[ "${ACTION}" == "help" || -z "${ACTION}" ]]; then
    log "showing '${SUBCOMMAND}' help"
    _help
  fi
}

_arg_subcmd=${1}
log "got argument '${_arg_subcmd}'"
case ${_arg_subcmd} in
  -l|--libs)
    log 'showing available libs'
    _list_libraries
  ;;
  help|-h|-?|--help|'')
    log 'help or no argument was given'
    _list_commands
  ;;
  --version)
    echo "${MAIN_COMMAND} ${MAIN_COMMAND_VERSION}"
  ;;
  --debug)
    DEBUG="true"
    log 'debug enabled using --debug'
    shift
    eval "${MAIN_COMMAND^^}_DEBUG=true ${MAIN_COMMAND} ${@}"
  ;;
  *)
    log "arguments '${*}'"
    log "checking if '${SUBCOMMANDS_DIR}/${_arg_subcmd}' exists"
    [[ ! -f "${SUBCOMMANDS_DIR}/${_arg_subcmd}" ]] && in_red "'${_arg_subcmd}' not found\n\n" && _list_commands
    shift 1
    _handle_subcommand ${_arg_subcmd} "${@}"
    ;;
esac
