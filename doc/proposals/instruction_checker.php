<?php
//author: alex temal, doug treadwell
//date: 2009-12-29
//url: http://www.aiyosolutions.com/dtnet/instruction_checker.php.txt

$instructions = file_get_contents('instructions.txt');

$lines = explode("\n", $instructions);

function line_is_section_header($line) {
	if ( ucwords($line) == $line && substr(trim($line), -1) == ':' ) {
		return true;
	} else {
		return false;
	}
}

function get_section($line) {
	return substr(strtolower(trim($line)), 0, -1);
}

function test_out($text) {
	print $text . '<br />';
}

function line_is_blank($line) {
	if ( trim($line) == '' ) {
		return true;
	} else {
		return false;
	}
}

function line_is_not_blank($line) {
	return !line_is_blank($line);
}

$equipment = array();
$materials = array();

foreach ( $lines as $line ) {
	++$line_number;
	if ( line_is_section_header($line) ) {
		$section = get_section($line);
		test_out('Identified section as ' . $section);
	} else if ( line_is_not_blank($line) ) { // is instruction
		test_out('Checking line ' . $line_number);
		if ( preg_match('/([0-9]+\.[0-9]*)(.*)/', $line, $matches) ) {
			list(/*don't need*/,$instruction_number, $instruction) = $matches;			
		} else {
			$instruction_number = '';
			$instruction = $line;
		}

		if ( $section == 'equipment' ) {
			test_out('Adding ' . $instruction . ' to ' . $section);
			$equipment[] = $instruction;
		} else if ( $section == 'materials' ) {
			test_out('Adding ' . $instruction . ' to ' . $section);
			$materials[] = $instruction;
		} else if ( $section == 'instructions' ) {
			test_out('Processing instruction " ' . $instruction . '"');
			$has_equipment = false;
			foreach ( $equipment as $tool ) {
				if ( strpos($instruction, $tool) !== false ) {
					$has_equipment = true;
					break;
				}
			}

			$has_materials = false;
			foreach ( $materials as $material ) {
				if ( strpos($instruction, $material) !== false ) {
					$has_materials = true;
					break;
				}
			}

			if ( !$has_equipment ) {
				print '&nbsp;&nbsp;No equipment specified on instruction ' . $instruction_number . '<br />';
			}
			if ( !$has_materials ) {
				print '&nbsp;&nbsp;No materials specified on instruction ' . $instruction_number . '<br />';
			}
			if ( $has_equipment && $has_materials ) {
				print '&nbsp;&nbsp;Instruction is ok.';
			}
		}

	}
}
?>
