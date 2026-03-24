import { ApiProperty } from '@nestjs/swagger';

export class CatSchema {
  @ApiProperty({ example: 1 })
  id: number;

  @ApiProperty({ example: 'Барсик' })
  name: string;

  @ApiProperty({ example: 3 })
  age: number;

  @ApiProperty({ example: 'Метис' })
  breed: string;

  @ApiProperty({ example: false })
  isAdopted: boolean;

  @ApiProperty({ example: 'Очень ласковый кот' })
  description: string;
}