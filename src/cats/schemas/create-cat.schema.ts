import { ApiProperty } from '@nestjs/swagger';
import { Cat } from '../interfaces/cat.interface';

export class CreateCatSchema implements Cat {
  @ApiProperty({ example: 'Tom', description: 'The name of the cat' })
  name: string;

  @ApiProperty({ example: 2, description: 'The age of the cat' })
  age: number;

  @ApiProperty({ example: 'Persian', description: 'The breed of the cat' })
  breed: string;
}